"""Optional real-browser QA against the running local HTTP report server.

Requires Playwright and an installed Edge browser; not part of the core runtime.
"""
import argparse
import csv
import json
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

parser=argparse.ArgumentParser()
parser.add_argument('--url',default='http://127.0.0.1:8000/data_quality_report.html')
args=parser.parse_args()
out=Path('reports/explorer/qa');out.mkdir(parents=True,exist_ok=True)
errors=[];checks=[]

with sync_playwright() as playwright:
    browser=playwright.chromium.launch(channel='msedge',headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},accept_downloads=True)
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.goto(args.url)
    expect(page.locator('#application')).to_be_visible(timeout=60000)
    page.wait_for_function('window.saguarodataExplorer !== undefined')
    assert page.evaluate('window.saguarodataExplorer.counts.observations')==63432
    assert page.evaluate('window.saguarodataExplorer.counts.findings')==8412
    checks.append('Full corpus counts agree with the canonical build')
    page.screenshot(path=str(out/'overview.png'),full_page=True)

    page.locator('[data-program-pick="historic_plots"]').click()
    page.select_option('#year','2014')
    assert page.evaluate('window.saguarodataExplorer.counts.selectedObservations')==2894
    page.locator('[data-tab="changes"]').click()
    page.select_option('#pair-interval','2010–2014')
    page.wait_for_function('pairsPlot && pairsPlot.points.length > 0')
    page.screenshot(path=str(out/'linked-changes.png'),full_page=True)
    point=page.evaluate('pairsPlot.points.find(p=>p.pair.height_after<p.pair.height_before*.8) || pairsPlot.points[0]')
    box=page.locator('#pairs').bounding_box()
    page.mouse.click(box['x']+point['x'],box['y']+point['y'])
    expect(page.locator('#detail')).to_be_visible()
    expect(page.locator('#detail-title')).to_contain_text('2014',timeout=15000)
    expect(page.locator('#detail-body')).to_contain_text('Source-supported individual history')
    assert page.locator('.history-point').count()>=2
    checks.append('Pair scatter opens a real record and supported full history')
    with page.expect_download() as info:page.locator('#detail-export').click()
    download=info.value;download.save_as(str(out/'evidence.json'))
    evidence=json.loads((out/'evidence.json').read_text())
    assert evidence['raw'] and evidence['transforms'] and evidence['canonical']['source_sha256']
    assert any(t['field']=='longitude,latitude' for t in evidence['transforms'])
    checks.append('Evidence JSON contains raw values, transformations and coordinate lineage')
    deep_link=page.url
    page.reload();expect(page.locator('#detail')).to_be_visible(timeout=30000)
    expect(page.locator('#detail-title')).to_contain_text('2014',timeout=15000)
    assert page.url==deep_link
    page.locator('[data-detail-tab="transforms"]').click()
    expect(page.locator('[data-detail-panel="transforms"]')).to_be_visible()
    page.screenshot(path=str(out/'evidence.png'))
    page.locator('#close-detail').click()
    checks.append('Deep links survive reload; raw/normalized evidence tabs work')

    page.locator('[data-tab="records"]').click()
    page.fill('#search','71G');page.wait_for_timeout(350)
    page.locator('#records-table button[data-entity]').first.click()
    expect(page.locator('#detail-body')).to_contain_text('Individual linkage is withheld on 71G',timeout=15000)
    assert page.locator('.history-point').count()==0
    page.locator('#close-detail').click()
    checks.append('71G has no invented individual history')

    page.locator('#reset').click();page.select_option('#program','section17');page.select_option('#year','1941')
    expect(page.locator('#scatter-caption')).to_contain_text('13,304 records have no numeric value')
    page.locator('[data-tab="overview"]').click()
    expect(page.locator('#coverage-chart')).to_contain_text('0 / 13,304')
    checks.append('Not-collected 1941 height is distinct from numeric zero')

    page.locator('#reset').click();page.locator('[data-tab="findings"]').click()
    page.select_option('#rule','UNKNOWN_SPATIAL_CRS')
    assert page.evaluate('window.saguarodataExplorer.counts.selectedFindings')==437
    with page.expect_download() as info:page.locator('#export-findings').click()
    info.value.save_as(str(out/'findings.csv'))
    with (out/'findings.csv').open(newline='',encoding='utf8') as stream:assert len(list(csv.DictReader(stream)))==437
    page.locator('#findings-table button[data-entity]').first.click()
    expect(page.locator('#detail-title')).not_to_have_text('Loading record…',timeout=15000)
    expect(page.locator('#detail-body')).to_contain_text('UNKNOWN_SPATIAL_CRS')
    page.locator('[data-profile-file]').click()
    expect(page.locator('#detail-body')).to_contain_text('Column profiles',timeout=30000)
    page.locator('#close-detail').click()
    checks.append('Every filtered spatial finding drills into source attributes and column profiles')

    page.locator('[data-tab="sources"]').click()
    expect(page.locator('#sources-table tbody tr')).to_have_count(25,timeout=30000)
    page.fill('#source-search','no-such-source-test')
    expect(page.locator('#sources-table')).to_contain_text('No source sheets or layers')
    page.fill('#source-search','HistoricPlot')
    expect(page.locator('#sources-table tbody tr').first).to_be_visible()
    page.locator('#sources-table button[data-source]').first.click()
    expect(page.locator('#detail-body')).to_contain_text('Column profiles')
    page.locator('#close-detail').click()
    checks.append('Lazy-loaded source inventory, search, empty state and drill-down work')

    page.locator('#reset').click();page.select_option('#program','historic_plots');page.select_option('#year','2014')
    page.locator('[data-tab="map"]').click();page.wait_for_function('mapPlot && mapPlot.points.length > 0')
    assert page.evaluate('mapPlot.points.some(p=>p.complete) && mapPlot.points.some(p=>!p.complete)')
    assert page.evaluate("mapPlot.points.filter(p=>p.row.organism_id).every(p=>p.coverage.count===new Set(organismIndex.get(p.row.organism_id).map(r=>r.survey_year)).size)")
    assert page.evaluate("mapPlot.points.filter(p=>p.complete).every(p=>p.coverage.count===4)")
    assert page.evaluate("new Set(mapPlot.points.map(p=>p.row.organism_id||p.row.observation_id)).size===mapPlot.points.length")
    expect(page.locator('#map-completeness-legend')).to_contain_text('1 survey round')
    expect(page.locator('#map-completeness-legend')).to_contain_text('4 survey rounds')
    assert page.evaluate("mapPlot.points.every(p=>p.marker==='cactus' && p.color===historyShade(p.coverage))")
    assert page.evaluate("new Set([1,2,3,4].map(count=>historyShade({count}))).size===4")
    assert page.evaluate("observationGreens.map(hex=>parseInt(hex.slice(1,3),16)).every((red,i,reds)=>!i||red<reds[i-1])")
    page.select_option('#map-color','finding')
    assert page.evaluate('mapPlot.points.some(p=>p.complete) && mapPlot.points.some(p=>!p.complete)')
    page.select_option('#map-color','program')
    checks.append('Map uses distinct whole-history round coverage and one marker per linked cactus, even with a year filter')
    before=page.evaluate('mapBounds[1]-mapBounds[0]');page.locator('#map-in').click()
    assert page.evaluate('mapBounds[1]-mapBounds[0]')<before
    page.locator('#map-reset').click()
    point=page.evaluate('mapPlot.points.find(p=>p.row.organism_id)');box=page.locator('#map').bounding_box()
    page.mouse.move(box['x']+point['x'],box['y']+point['y'])
    expect(page.locator('#map-tip')).to_be_visible()
    expect(page.locator('#map-tip')).to_contain_text('survey rounds',ignore_case=True)
    page.screenshot(path=str(out/'map.png'),full_page=True)
    page.mouse.click(box['x']+point['x'],box['y']+point['y'])
    expect(page.locator('#detail-title')).to_contain_text('2014',timeout=15000)
    page.locator('#close-detail').click()
    expect(page.locator('#colocated')).to_contain_text('records at')
    checks.append('Geographic map zoom, hover, point selection and co-location drill-down work')
    page.wait_for_function('mapContext && regionalBackgrounds.has("topo")',timeout=30000)
    assert page.evaluate('mapContext.layers.parks.length')==2
    assert page.evaluate('mapContext.layers.city.length')==1
    assert page.evaluate('mapContext.layers.roads.length')>100
    page.locator('#map-region').click()
    assert page.evaluate('mapBounds[1]-mapBounds[0]')>.8
    # The returned raster extent must be geographic and include the requested view.
    page.wait_for_function('Array.from(mapBackgrounds.values()).some(v=>v && v.extent.spatialReference.wkid===4326)',timeout=45000)
    for layer in ['parks','city','roads','plots','labels']:
        control=page.locator(f'[data-map-layer="{layer}"]')
        control.uncheck();assert page.evaluate(f'mapLayers.{layer}') is False
        control.check();assert page.evaluate(f'mapLayers.{layer}') is True
    expect(page.locator('#map-background-status')).to_contain_text('Map detail loaded',timeout=45000)
    page.screenshot(path=str(out/'tucson-topographic.png'),full_page=True)
    page.select_option('#map-background','relief')
    page.wait_for_function('regionalBackgrounds.has("relief")')
    expect(page.locator('#map-background-status')).to_contain_text('Shaded relief')
    expect(page.locator('#map-background-status')).to_contain_text('Map detail loaded',timeout=45000)
    page.screenshot(path=str(out/'tucson-relief.png'),full_page=True)
    # Local fallback remains available when external terrain services fail.
    page.route('https://basemap.nationalmap.gov/**',lambda route:route.abort())
    page.select_option('#map-background','topo');page.locator('#map-in').click()
    page.wait_for_function('Array.from(mapBackgrounds.values()).some(v=>v===null)',timeout=30000)
    expect(page.locator('#map-background-status')).to_contain_text('local regional snapshot',ignore_case=True)
    page.unroute('https://basemap.nationalmap.gov/**')
    page.select_option('#map-background','none')
    expect(page.locator('#map-background-status')).to_contain_text('Plain coordinate view')
    page.locator('#map-reset').click()
    checks.append('Official city/park/road overlays toggle; topography, relief, regional view and offline fallback work')

    page.locator('[data-tab="records"]').click()
    with page.expect_download() as info:page.locator('#export-records').click()
    info.value.save_as(str(out/'observations.csv'))
    with (out/'observations.csv').open(newline='',encoding='utf8') as stream:assert len(list(csv.DictReader(stream)))==2894
    page.locator('[data-sort="height_m"]').click()
    page.locator('[data-page-key="pageObs"][data-page-delta="1"]').click()
    expect(page.locator('#records-pagination')).to_contain_text('26–50')
    checks.append('Filtered observation export, numeric sorting and pagination work')

    page.locator('#reset').click();page.locator('.tabs [data-tab="summaries"]').click()
    assert page.evaluate('visibleSummaries.length')==45
    page.locator('#summaries-table button[data-entity]').first.click()
    expect(page.locator('#detail-title')).to_contain_text('Plot summary',timeout=15000)
    expect(page.locator('#detail-body')).to_contain_text('Count estimate')
    assert page.evaluate("Object.values(selectedDetail.raw).some(v=>v!=='' && Number.isFinite(Number(v)) && !Number.isInteger(Number(v)))")
    page.locator('#close-detail').click()
    page.select_option('#summary-kind','vegetation');page.select_option('#year','2010')
    assert page.evaluate('visibleSummaries.length')==830
    page.fill('#summary-search','CAGI')
    assert page.evaluate('visibleSummaries.length')>0
    page.locator('#summaries-table button[data-entity]').first.click()
    expect(page.locator('#detail-title')).to_contain_text('Vegetation',timeout=15000)
    expect(page.locator('#detail-body')).to_contain_text('Raw cover')
    assert page.locator('.history-point').count()==0
    page.locator('#close-detail').click()
    checks.append('Fractional source height-class estimates are preserved; vegetation has separate source evidence')

    page.set_viewport_size({'width':390,'height':844})
    page.goto(args.url);expect(page.locator('#application')).to_be_visible(timeout=60000)
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1')
    page.screenshot(path=str(out/'mobile.png'),full_page=True)
    page.locator('[data-tab="findings"]').click()
    page.select_option('#severity','error')
    expect(page.locator('#findings-table button[data-entity]').first).to_be_visible()
    checks.append('Mobile layout has no document overflow; controls remain usable')
    assert not errors,errors
    browser.close()

result=dict(checks=checks,browser_errors=errors)
(out/'checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
