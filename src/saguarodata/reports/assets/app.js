/* Local, dependency-free exploration. Full source evidence is fetched on demand. */
'use strict';
const $ = id => document.getElementById(id);
const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt = value => value == null ? '—' : Number(value).toLocaleString(undefined, {maximumFractionDigits: 3});
const pretty = value => JSON.stringify(value, null, 2);
const present = value => value !== null && value !== undefined && Number.isFinite(Number(value));
const names = {census:'Census', census_auxiliary:'Census · auxiliary', historic_plots:'Historic Plots', section17:'Section 17', ecotone:'Ecotone', vegetation:'Vegetation', census_summary_auxiliary:'Auxiliary summaries', boundaries:'Boundaries'};
const colors = {census:'#557f9c',census_auxiliary:'#8d819c',historic_plots:'#42745b',section17:'#ba8950',ecotone:'#a15e6d',vegetation:'#6e8d55',boundaries:'#7b827b'};
const severityColors = {error:'#ad5546',warning:'#c79435',info:'#557f9c',none:'#a9b5a8'};
const observationGreens=['#b8dca0','#83b96f','#438b4c','#145a32'];
const cactusOutline='M6 16V10H4C2 10 1 9 1 7V5C1 3 4 3 4 5V7H6V2C6 -1 10 -1 10 2V9H12V6C12 4 15 4 15 6V9C15 11 14 12 12 12H10V16Z';
const cactusPath=new Path2D(cactusOutline);
const historyShade=coverage=>coverage.count===null?'#919b94':observationGreens[Math.min(4,Math.max(1,coverage.count))-1];
const historyNames={full:'All survey rounds',partial:'3+ rounds · incomplete',short:'1–2 rounds · incomplete',unlinked:'History unknown · unlinked'};
const historyCoverage=new Map();
const label = program => names[program] || program || 'Undated source layer';
const PAGE = 25;
const state = {tab:'overview',program:'',year:'',q:'',rule:'',severity:'',mode:'all',measure:'height_m',coverageField:'height_m',pairMeasure:'height',pairInterval:'',summaryKind:'plot',representation:'RawData_1990_Total_Saguaros',summaryQ:'',pageSummary:0,pagePairs:0,pageObs:0,pageFind:0,pageSource:0,sort:'survey_year',direction:-1,sourceQ:'',entity:'',fi:''};
let data, observations, findings, obsIndex, organismIndex, entityFindings, sources, sourcesPromise;
let baseRecords=[], baseFindings=[], visibleRecords=[], visibleFindings=[], visibleSources=[];
let scatterBounds=null, scatterPlot=null, mapBounds=null, mapPlot=null, selectedDetail=null, detailToken=0;
let mapContext=null,mapContextPromise=null,mapContextFailed=false;
const mapBackgrounds=new Map(),regionalBackgrounds=new Map();
let backgroundTimer=null,backgroundRequest=0;
function loadRegionalBackgrounds() {
  for(const [kind,metadata] of Object.entries(mapContext.backgrounds||{})){
    const img=new Image();img.onload=()=>{regionalBackgrounds.set(kind,{image:img,extent:metadata.extent});if(state.tab==='map')drawMap();};
    img.src='explorer/'+metadata.file;
  }
}
function drawMapBackground(ctx,x,y,width,height,sx,sy,cx,cy) {
  const kind=$('map-background').value;
  if(kind==='none'){$('map-background-status').textContent='Plain coordinate view · geographic layers are stored locally.';return;}
  if(!mapContext)return;
  const metadata=mapContext.backgrounds?.[kind];if(!metadata)return;
  const bounds=[cx-width/2/sx,cy-height/2/sy,cx+width/2/sx,cy+height/2/sy];
  const key=kind+':'+bounds.map(n=>n.toFixed(7)).join(',')+':'+Math.round(width)+':'+Math.round(height);
  const cached=mapBackgrounds.get(key);
  const frame=cached||regionalBackgrounds.get(kind);
  if(frame){const e=frame.extent;ctx.drawImage(frame.image,x(e.xmin),y(e.ymax),x(e.xmax)-x(e.xmin),y(e.ymin)-y(e.ymax));}
  $('map-background-status').textContent=`${metadata.attribution} · ${cached?'Map detail loaded':cached===null?'Using local regional snapshot; live detail unavailable':'Local regional snapshot; loading detail…'} · ${kind==='topo'?'Contours show ground elevation in the units printed on the map.':'Shaded relief shows terrain shape; it is not a numeric elevation measurement.'}`;
  clearTimeout(backgroundTimer);
  if(mapBackgrounds.has(key))return;
  const request=++backgroundRequest;
  backgroundTimer=setTimeout(async()=>{
    // ArcGIS may expand the requested bbox to match its image aspect ratio.
    try{
      const params=new URLSearchParams({bbox:bounds.join(','),bboxSR:'4326',imageSR:'4326',size:`${Math.round(width)},${Math.round(height)}`,format:'jpg',f:'json'});
      const response=await fetch(metadata.service+'/export?'+params, {signal:AbortSignal.timeout(20000)});
      if(!response.ok)throw new Error('Map service unavailable');
      const info=await response.json();if(!info.href||!info.extent)throw new Error('Invalid map image');
      const img=await new Promise((resolve,reject)=>{const image=new Image();image.onload=()=>resolve(image);image.onerror=reject;image.src=info.href;});
      mapBackgrounds.set(key,{image:img,extent:info.extent});
      if(mapBackgrounds.size>12)mapBackgrounds.delete(mapBackgrounds.keys().next().value);
    }catch(error){mapBackgrounds.set(key,null);}
    if(request===backgroundRequest&&state.tab==='map')drawMap();
  },250);
}
const mapLayers={parks:true,city:true,roads:true,plots:true,labels:true};
function ensureMapContext() {
  if(mapContext || mapContextPromise || mapContextFailed)return;
  $('map-context-status').textContent='Loading local geographic context…';
  mapContextPromise=fetch('explorer/geographic_context.json').then(response=>{
    if(!response.ok)throw new Error('Geographic context unavailable');return response.json();
  }).then(value=>{
    mapContext=value;
    loadRegionalBackgrounds();
    const dates=[...new Set(value.sources.map(source=>source.retrieved_utc.slice(0,10)))];
    $('map-context-status').innerHTML=`Local context snapshot · ${esc(dates.join(', '))}. Boundaries and roads show current geography, not historical survey conditions. Sources: <a href="https://irma.nps.gov/DataStore/DownloadFile/754039" target="_blank" rel="noopener">NPS boundary data</a> · <a href="https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Places_CouSub_ConCity_SubMCD/MapServer/4" target="_blank" rel="noopener">U.S. Census Bureau city limits</a> · <a href="https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/Transportation/MapServer" target="_blank" rel="noopener">Census roads</a>. Roads cover the Tucson region only.`;
    if(state.tab==='map')drawMap();
  }).catch(()=>{mapContextFailed=true;$('map-context-status').textContent='Geographic context could not be loaded. Observation points and source plots remain available.';});
}
function contextLines(geometry) {
  if(geometry.type==='LineString')return [geometry.coordinates];
  if(geometry.type==='MultiLineString'||geometry.type==='Polygon')return geometry.coordinates;
  if(geometry.type==='MultiPolygon')return geometry.coordinates.flat();
  if(geometry.type==='GeometryCollection')return geometry.geometries.flatMap(contextLines);
  return [];
}
function drawMapContext(ctx,x,y,width,height,sx) {
  if(!mapContext)return;
  const labelBoxes=[];
  function text(text,px,py,color,size=12) {
    ctx.font=`600 ${size}px system-ui`;const w=ctx.measureText(text).width;
    const box=[px-3,py-size-2,px+w+3,py+4];
    if(box[0]<5||box[2]>width-5||box[1]<20||box[3]>height-35||labelBoxes.some(b=>box[0]<b[2]&&box[2]>b[0]&&box[1]<b[3]&&box[3]>b[1]))return;
    labelBoxes.push(box);ctx.lineWidth=4;ctx.strokeStyle='#f5f5ef';ctx.strokeText(text,px,py);ctx.fillStyle=color;ctx.fillText(text,px,py);
  }
  for(const key of ['city','parks','roads']) {
    if(!mapLayers[key])continue;
    const features=key==='roads'?[...mapContext.layers[key]].sort((a,b)=>({local:0,secondary:1,primary:2}[a.properties.kind])-({local:0,secondary:1,primary:2}[b.properties.kind])):mapContext.layers[key];
    for(const feature of features) {
      const kind=feature.properties.kind;
      if(kind==='local'&&sx<4500)continue;
      const lines=contextLines(feature.geometry);
      ctx.beginPath();
      for(const line of lines)line.forEach((coord,i)=>i?ctx.lineTo(x(coord[0]),y(coord[1])):ctx.moveTo(x(coord[0]),y(coord[1])));
      if(key!=='roads'){ctx.fillStyle=key==='parks'?'#78a26f18':'#7d9fb614';ctx.fill('evenodd');}
      ctx.strokeStyle=key==='parks'?'#61834d':key==='city'?'#6a91ac':kind==='primary'?'#ba936b':kind==='secondary'?'#b6a38b':'#d2c9ba';
      ctx.lineWidth=key==='roads'?(kind==='primary'?2.8:kind==='secondary'?1.7:.8):1.8;
      ctx.setLineDash(key==='city'?[7,4]:[]);ctx.stroke();ctx.setLineDash([]);
    }
  }
  if(mapLayers.labels) {
    // Label positions are display anchors; boundaries always come from source geometry.
    if(mapLayers.city)text('TUCSON',x(-110.97),y(32.22),'#52758e',15);
    if(mapLayers.parks){text('SAGUARO · TUCSON MOUNTAIN',x(-111.22),y(32.305),'#537443');text('SAGUARO · RINCON MOUNTAIN',x(-110.70),y(32.22),'#537443');}
    if(mapLayers.roads){
      const seen=new Set();
      for(const feature of mapContext.layers.roads){
        if(feature.properties.kind==='local'&&sx<16000)continue;
        if(seen.has(feature.properties.name)||feature.properties.name==='Unnamed road')continue;
        let best=null,bestLength=0;
        for(const line of contextLines(feature.geometry))for(let i=1;i<line.length;i++){
          const a=[x(line[i-1][0]),y(line[i-1][1])],b=[x(line[i][0]),y(line[i][1])];
          const length=Math.hypot(a[0]-b[0],a[1]-b[1]);
          const mid=[(a[0]+b[0])/2,(a[1]+b[1])/2];
          if(length>bestLength&&mid[0]>30&&mid[0]<width-90&&mid[1]>30&&mid[1]<height-40){best=mid;bestLength=length;}
        }
        if(best&&bestLength>35){text(feature.properties.name,best[0],best[1]-5,'#877258',10);seen.add(feature.properties.name);}
      }
    }
  }
  // Approximate local scale in this longitude-scaled geographic view.
  const kmPerPixel=111.32*Math.cos(32.2*Math.PI/180)/sx;
  const km=niceStep(kmPerPixel*130,1),px=km/kmPerPixel;
  ctx.fillStyle='#fffefaee';ctx.fillRect(13,height-65,Math.max(px+18,85),32);
  ctx.strokeStyle='#526253';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(22,height-53);ctx.lineTo(22,height-45);ctx.lineTo(22+px,height-45);ctx.lineTo(22+px,height-53);ctx.stroke();
  ctx.font='10px system-ui';ctx.fillStyle='#526253';ctx.fillText(km<1?`${Math.round(km*1000)} m`:`${fmt(km)} km`,22,height-56);
  ctx.fillText('N ↑',width-35,32);
}
let pairsPlot=null,visiblePairs=[];
let summaryRows={},visibleSummaries=[];
let photoCatalog=null,photoPromise=null,visiblePhotos=[];
let activeLineage=null;
function lineagePanel(detail) {
  const fields=[...new Set(detail.transforms.map(t=>t.field))];
  return `<details class="lineage-panel"><summary>Explore executable evidence lineage</summary><p class="caption">A focused evidence slice, derived from the canonical provenance tables. Arrows run from source evidence to the derived value. A finding trace includes every explicitly referenced prior record; shared source rows are not independent samples.</p><div class="toolbar"><label>Canonical field<select id="lineage-field">${fields.map(field=>`<option>${esc(field)}</option>`).join('')||'<option value="">Source row only</option>'}</select></label><button id="lineage-observation">Trace selected field</button><button id="lineage-download" disabled>Export trace JSON</button></div><div id="lineage-view" aria-live="polite"></div></details>`;
}
async function showLineage(findingId=null) {
  const detail=selectedDetail,token=detailToken;
  if(!detail)return;
  document.querySelector('.lineage-panel').open=true;
  $('lineage-view').innerHTML='<p class="caption">Loading contributing evidence…</p>';
  const finding=findingId?detail.findings.find(f=>f.finding_id===findingId):null;
  const value=finding?.observed_value||{};
  const previous=[value.previous,value.previous_observation_id,value.previous_feature,...(finding?.lineage_context?.entities||[])].filter(v=>typeof v==='string');
  const details=[detail];const missing=[];
  for(const entity of [...new Set(previous)]){
    try{details.push(await loadDetail(entity));}catch{missing.push(entity);}
  }
  if(token!==detailToken)return;
  let field=finding?.field||$('lineage-field').value;
  if([...$('lineage-field').options].some(option=>option.value===field))$('lineage-field').value=field;
  const nodes=new Map(),edges=new Map();
  const selectedByRecord=[];
  for(const record of details){
    const local=record.lineage;
    if(!local){missing.push(record.canonical.observation_id||record.canonical.feature_id);continue;}
    const ns=new Map(local.nodes.map(([id,type,label,attributes])=>[id,{id,type,label,attributes}]));
    const es=local.edges.map(([id,source,target,type])=>({id,source,target,type}));
    const roots=[...ns.values()].filter(n=>n.type==='canonical_field'&&field.split(',').includes(n.attributes.field)).map(n=>n.id);
    if(!roots.length)roots.push(local.root);
    const keep=new Set(roots),queue=[...roots];
    while(queue.length){const id=queue.pop();for(const edge of es)if(edge.target===id&&!keep.has(edge.source)){keep.add(edge.source);queue.push(edge.source);}}
    keep.add(local.root);for(const id of keep)if(ns.has(id))nodes.set(id,ns.get(id));
    for(const edge of es)if(keep.has(edge.source)&&keep.has(edge.target))edges.set(edge.id,edge);
    selectedByRecord.push({record,nodes:[...keep].map(id=>ns.get(id)).filter(Boolean)});
  }
  if(finding){
    for(const [id,type,label,attributes] of finding.lineage_context?.nodes||[])nodes.set(id,{id,type,label,attributes});
    for(const [id,source,target,type] of finding.lineage_context?.edges||[])if(nodes.has(source)&&nodes.has(target))edges.set(id,{id,source,target,type});
    const id=finding.lineage_node_id;
    nodes.set(id,{id,type:'validation_finding',label:finding.rule_id,attributes:finding});
    for(const [eid,source,target,type] of finding.lineage_edges||[])if(nodes.has(source)&&nodes.has(target))edges.set(eid,{id:eid,source,target,type});
  }
  activeLineage={root:finding?.lineage_node_id||detail.lineage?.root,finding_id:finding?.finding_id||null,field,nodes:[...nodes.values()],edges:[...edges.values()],missing_evidence:missing};
  $('lineage-download').disabled=false;document.querySelector('.lineage-panel').scrollIntoView({block:'start',behavior:'smooth'});
  $('lineage-view').innerHTML=`${finding?`<h3>${esc(finding.rule_id)} · ${esc(finding.finding_id)}</h3>`:''}${selectedByRecord.map(({record,nodes})=>{
    const row=record.canonical;const cells=nodes.filter(n=>n.type==='source_field');const transforms=nodes.filter(n=>n.type==='transformation');const fields=nodes.filter(n=>n.type==='canonical_field');
    return `<article class="lineage-branch"><h3><button class="textbutton" data-entity="${esc(row.observation_id||row.feature_id)}">${esc(row.survey_year||'Source feature')} · ${esc(row.plot_id||row.layer||'')} · ${esc(row.observation_id||row.feature_id)}</button></h3><div class="lineage-flow"><div><small>SOURCE ROW / CELL</small><strong>${esc(row.source_sheet)} · row ${fmt(row.source_row)}</strong>${cells.map(n=>`<p>${esc(n.attributes.source_column)}${n.attributes.exists_in_source===false?' (not found in source sheet)':''} = <code>${esc(n.attributes.value??'null')}</code></p>`).join('')}</div><span aria-hidden="true">→</span><div><small>RECORDED TRANSFORMATION</small>${transforms.length?transforms.map(n=>`<p><strong>${esc(n.attributes.transformation||'missing')}</strong><br>${esc(n.attributes.value_kind)}</p>`).join(''):'<p>Source-row lineage only; no field transformation recorded.</p>'}</div><span aria-hidden="true">→</span><div><small>CANONICAL VALUE</small>${fields.map(n=>`<p><strong>${esc(n.attributes.field)}</strong> = <code>${esc(typeof n.attributes.value==='object'?pretty(n.attributes.value):n.attributes.value??'null')}</code></p>`).join('')||'<p>Source record</p>'}</div></div></article>`;
  }).join('')}<div class="lineage-artifacts">${[...nodes.values()].filter(n=>n.type==='source_artifact').map(n=>`<p><strong>${esc(n.attributes.filename)}</strong><br><code>SHA-256 ${esc(n.attributes.sha256)}</code><br><a href="${esc(n.attributes.source_url)}" target="_blank" rel="noopener">Original NPS reference ↗</a></p>`).join('')}</div>${missing.length?`<p class="finding-card error">Missing evidence: ${esc(missing.join(', '))}. Trace is incomplete.</p>`:''}`;
}
const shardCache = new Map();
const hashKeys=['tab','program','year','q','rule','severity','mode','pairMeasure','pairInterval','summaryKind','representation','entity','fi'];
state.mapBackground='topo';state.mapView='records';
hashKeys.push('mapBackground','mapView');
state.photoQ='';state.photoLicense='';state.pagePhotos=0;
hashKeys.push('photoQ','photoLicense');

function readHash() {
  const params=new URLSearchParams(location.hash.slice(1));
  for (const key of hashKeys) if(params.has(key)) state[key]=params.get(key);
  if(!['overview','changes','records','summaries','findings','map','sources','photos'].includes(state.tab)) state.tab='overview';
  if(!['topo','relief','none'].includes(state.mapBackground))state.mapBackground='topo';
  if(!['records','region'].includes(state.mapView))state.mapView='records';
}
function syncHash() {
  const params=new URLSearchParams();
  for(const key of hashKeys) if(state[key] && !(key==='tab' && state[key]==='overview')) params.set(key,state[key]);
  history.replaceState(null,'',location.pathname+location.search+(params.size?'#'+params.toString():''));
}
function toast(message) { $('toast').textContent=message; $('toast').hidden=false; clearTimeout(toast.timer); toast.timer=setTimeout(()=>$('toast').hidden=true,3000); }
async function copyLink() {
  syncHash();
  try { await navigator.clipboard.writeText(location.href); toast('Link copied with the current filters and selected record.'); }
  catch { toast('Copy the address in your browser to share this view.'); }
}
function unpack(columns, rows) { return rows.map(row=>Object.fromEntries(columns.map((key,i)=>[key,row[i]]))); }
function badge(text, kind=text) { return `<span class="badge ${esc(kind)}">${esc(text)}</span>`; }
function empty(message) { return `<div class="empty">${esc(message)}</div>`; }
function textSearch(row) { return [row.observation_id,row.source_individual_id,row.plot_id].join(' ').toLowerCase(); }
function recordMatches(row, ignoreProgram=false) {
  return (ignoreProgram || !state.program || row.program_id===state.program) &&
    (!state.year || String(row.survey_year)===state.year) && (!state.q || textSearch(row).includes(state.q.toLowerCase()));
}
function findingMatches(row) {
  if(state.program && row.program_id!==state.program) return false;
  if(state.year && String(row.survey_year)!==state.year) return false;
  if(state.q) {
    const observation=obsIndex.get(row.entity_identifier);
    if(!(observation?textSearch(observation):row.entity_identifier).toLowerCase().includes(state.q.toLowerCase())) return false;
  }
  return true;
}
function recordMode(row) {
  if(state.mode==='flagged') return entityFindings.has(row.observation_id);
  if(state.mode==='linked') return Boolean(row.organism_id);
  if(state.mode==='height_missing') return row.height_m===null;
  if(state.mode==='arms_missing') return row.arm_count===null;
  return true;
}
function setTab(tab) { state.tab=tab; render(); }
function updateScope(changes) {
  Object.assign(state,changes,{pageObs:0,pageFind:0,pageSource:0,pagePairs:0,pageSummary:0});
  scatterBounds=null; mapBounds=null;
  $('colocated').innerHTML='';
  render();
}
function render() {
  baseRecords=observations.filter(row=>recordMatches(row));
  baseFindings=findings.filter(findingMatches);
  visibleRecords=baseRecords.filter(recordMode);
  visibleFindings=baseFindings.filter(row=>(!state.rule||row.rule_id===state.rule)&&(!state.severity||row.severity===state.severity));
  for(const key of ['program','year','rule','severity']) $(key).value=state[key];
  $('search').value=state.q; $('record-mode').value=state.mode; $('measure').value=state.measure;
  document.querySelectorAll('.tabs [data-tab]').forEach(button=>button.setAttribute('aria-selected',String(button.dataset.tab===state.tab)));
  for(const tab of ['overview','changes','records','summaries','findings','map','sources','photos']) $('view-'+tab).hidden=state.tab!==tab;
  $('filter-summary').textContent=`${state.program?label(state.program):'All sampling frames'} · ${state.year?'source year '+state.year:'all source years'} · ${fmt(baseRecords.length)} organism observations${state.q?' · matching “'+state.q+'”':''}`;
  for(const kind of ['plot','vegetation']) {
    const count=summaryRows[kind].filter(summaryMatches).length;
    if(count){const button=document.createElement('button');button.className='textbutton';button.dataset.tab='summaries';button.dataset.summaryKind=kind;button.textContent=`${fmt(count)} ${kind==='plot'?'aggregate representations':'vegetation summaries'} →`;button.style.marginLeft='12px';$('filter-summary').append(button);}
  }
  syncHash();
  if(state.tab==='overview') renderOverview();
  if(state.tab==='changes') requestAnimationFrame(renderPairs);
  if(state.tab==='summaries') renderSummaries();
  if(state.tab==='records') { renderRecords(); requestAnimationFrame(drawScatter); }
  if(state.tab==='findings') renderFindings();
  if(state.tab==='map') requestAnimationFrame(drawMap);
  if(state.tab==='sources') renderSources();
  if(state.tab==='photos') renderPhotos();
}
function photoLink(url,title) {
  try{
    const parsed=new URL(url);
    if(parsed.protocol!=='https:'||!['www.inaturalist.org','static.inaturalist.org','inaturalist-open-data.s3.amazonaws.com'].includes(parsed.hostname))return esc(title+' unavailable');
    return `<a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(title)} ↗</a>`;
  }catch{return esc(title+' unavailable');}
}
async function renderPhotos() {
  const references=data.photo_references||[];
  $('photo-references').innerHTML=references.length?`<table><thead><tr><th>Open source record</th><th>Original field / note</th><th>Original workbook</th></tr></thead><tbody>${references.map(row=>{
    const file=data.files.find(file=>file.local_filename===row.source_file);
    return `<tr><td><button class="textbutton" data-entity="${esc(row.observation_id)}">${esc(label(row.program_id))} · ${esc(row.plot_id)} · ${esc(row.source_individual_id||'source row '+row.source_row)}</button></td><td>${Object.entries(row.mentions).map(([key,value])=>`<strong>${esc(key)}</strong>: ${esc(value)}`).join('<br>')}</td><td>${file?`<a href="${esc(file.direct_download_url)}" target="_blank" rel="noopener">${esc(file.filename)} ↗</a>`:''}<br>${esc(row.source_sheet)} · row ${row.source_row}</td></tr>`;
  }).join('')}</tbody></table>`:empty('No photo references found in the NPS source rows.');
  $('photo-search').value=state.photoQ;
  $('export-photo-links').disabled=true;
  try{
    if(!photoCatalog){
      $('photo-status').textContent='Loading local photo-link metadata…';
      if(!photoPromise)photoPromise=fetch('explorer/photo_links.json').then(response=>{
        if(!response.ok)throw new Error('Photo-link catalog unavailable');return response.json();
      }).then(value=>photoCatalog=value).catch(error=>{photoPromise=null;throw error;});
      await photoPromise;
    }
    if(state.tab!=='photos')return;
    $('photo-license').innerHTML='<option value="">All licenses</option>'+[...new Set(photoCatalog.photos.map(row=>row.license))].sort().map(license=>`<option value="${esc(license)}">${esc(license.toUpperCase())}</option>`).join('');
    if(![...$('photo-license').options].some(option=>option.value===state.photoLicense))state.photoLicense='';
    $('photo-license').value=state.photoLicense;
    const query=state.photoQ.trim().toLowerCase();
    visiblePhotos=photoCatalog.photos.filter(row=>(!state.photoLicense||row.license===state.photoLicense)&&(!query||[row.observation_id,row.photo_id,row.attribution].join(' ').toLowerCase().includes(query)));
    $('photo-status').textContent=`${fmt(visiblePhotos.length)} / ${fmt(photoCatalog.photos.length)} photo links · ${fmt(new Set(visiblePhotos.map(row=>row.observation_id)).size)} matching iNaturalist observations. Links open the original provider; no images are fetched by this report.`;
    $('photo-links-table').innerHTML=visiblePhotos.length?`<table><thead><tr><th>iNaturalist observation</th><th>Photo</th><th>Photographer / attribution</th><th>License</th><th>Original sources</th></tr></thead><tbody>${pageRows(visiblePhotos,'pagePhotos').map(row=>`<tr><td>${photoLink(row.observation_url,String(row.observation_id))}</td><td>${row.photo_id}</td><td>${esc(row.attribution)}</td><td>${esc(row.license.toUpperCase())}</td><td><div class="photo-source-links">${photoLink(row.photo_page_url,'Photo page')}${photoLink(row.image_url,'Image at source')}</div></td></tr>`).join('')}</tbody></table>`:empty('No photos match this search and license filter.');
    pagination('photo-links-pagination',visiblePhotos,'pagePhotos');
    $('export-photo-links').disabled=false;syncHash();
  }catch(error){$('photo-status').textContent='The iNaturalist link catalog could not be loaded. Historical collection links above remain available.';$('photo-links-table').innerHTML='';$('photo-links-pagination').innerHTML='';}
}
function photoEvidenceHTML(detail) {
  const mentions=Object.entries(detail.raw||{}).filter(([key,value])=>/\bphoto(?:graph)?s?\b/i.test(String(value)));
  if(detail.kind!=='observation'&&!mentions.length)return '';
  const row=detail.canonical;
  const file=data.files.find(file=>file.local_filename===row.source_file);
  const identifier=[row.source_individual_id?`cactus ${row.source_individual_id}`:'this source observation',row.source_plot_id?`plot ${row.source_plot_id}`:row.plot_id,row.survey_year].filter(Boolean).join(' · ');
  return `<section class="observation-photos" aria-label="Photos for this observation"><h3>Photos for this observation</h3><p><strong>${esc(identifier)}</strong><br>No verified photo link has been found for this cactus in the acquired sources.</p>${mentions.length?`<p class="caption">The original row mentions photography. These notes may refer to another survey year represented in the row:</p>${mentions.map(([key,value])=>`<p class="caption"><strong>${esc(key)}</strong>: ${esc(value)}</p>`).join('')}`:''}<div class="photo-source-links">${file?`<a href="${esc(file.source_url)}" target="_blank" rel="noopener">Original NPS source record ↗</a>`:''}<a href="https://www.nps.gov/sagu/learn/nature/long-term-monitoring.htm" target="_blank" rel="noopener">NPS historical photos · landscape context ↗</a><a href="https://www.usgs.gov/media/slideshows/repeat-photographs-saguaro-national-monument-east-now-saguaro-national-park-rincon" target="_blank" rel="noopener">USGS repeat photos · landscape context ↗</a></div><p class="caption">Landscape photos and the separate iNaturalist collection are not verified images of this individual.</p><button data-photo-browse="true">Browse all photo sources</button></section>`;
}
function tally(rows, field) {
  const counts=new Map();
  for(const row of rows) counts.set(row[field],(counts.get(row[field])||0)+1);
  return [...counts].sort((a,b)=>b[1]-a[1]);
}
function barHTML(key,count,max,color,kind,name) {
  return `<button class="bar" data-${kind}="${esc(key)}" title="Filter to ${esc(name)}"><span class="bar-label">${esc(name)}</span><span class="bar-track"><span class="bar-fill" style="width:${100*count/max}%;background:${color}"></span></span><span class="bar-number">${fmt(count)}</span></button>`;
}
function renderOverview() {
  const flagged=baseRecords.filter(r=>entityFindings.has(r.observation_id)).length;
  const linked=new Set(baseRecords.map(r=>r.organism_id).filter(Boolean)).size;
  const n=baseRecords.length;
  const metrics=[['Organism observations',fmt(n),'Raw sampling frames remain distinct'],['Records with findings',fmt(flagged),`${n?(100*flagged/n).toFixed(1):'0'}% of selected observations · any severity`],['Validation findings',fmt(baseFindings.length),'Includes undated spatial findings when no year is selected'],['Linked organisms',fmt(linked),'Supported histories · 71G excluded']];
  $('metrics').innerHTML=metrics.map(([title,value,detail])=>`<div class="metric"><span class="label">${esc(title)}</span><span class="value">${value}</span><span class="small">${esc(detail)}</span></div>`).join('');
  const programs=tally(observations.filter(r=>recordMatches(r,true)),'program_id');
  $('program-chart').innerHTML=programs.length?programs.map(([program,count])=>barHTML(program,count,programs[0][1],colors[program]||'#42745b','program-pick',label(program))).join(''):empty('No observations match these filters.');
  const rules=tally(baseFindings,'rule_id');
  $('rule-chart').innerHTML=rules.length?rules.slice(0,8).map(([rule,count])=>barHTML(rule,count,rules[0][1],'#ba8950','rule-pick',rule.replaceAll('_',' ').toLowerCase())).join('')+(rules.length>8?`<p class="caption">Showing the 8 most frequent of ${rules.length} rules. Open all findings for the complete register.</p>`:''):empty('No findings match this scope. This does not mean every possible rule was applicable.');
  renderCoverage();
}
function renderCoverage() {
  const years=[...new Set(baseRecords.map(r=>r.survey_year))].sort((a,b)=>a-b);
  const programs=[...new Set(baseRecords.map(r=>r.program_id))];
  if(!years.length) { $('coverage-chart').innerHTML=empty('No observations to profile.'); return; }
  const reasonField=state.coverageField==='height_m'?'height_missing_reason':'arm_count_missing_reason';
  const groups=new Map();
  for(const row of baseRecords) {
    const key=row.program_id+'|'+row.survey_year;
    if(!groups.has(key)) groups.set(key,{n:0,valid:0,notCollected:0});
    const group=groups.get(key); group.n++;
    if(row[state.coverageField]!==null) group.valid++;
    else if(String(row[reasonField]||'').startsWith('not_collected')) group.notCollected++;
  }
  $('coverage-chart').innerHTML=`<table class="coverage-table"><thead><tr><th>Sampling frame</th>${years.map(y=>`<th>${y}</th>`).join('')}</tr></thead><tbody>${programs.map(program=>`<tr><th>${esc(label(program))}</th>${years.map(year=>{
    const group=groups.get(program+'|'+year);
    if(!group) return '<td class="empty">—</td>';
    const missing=group.n-group.valid-group.notCollected;
    return `<td><button class="coverage-cell" data-cell-program="${esc(program)}" data-cell-year="${year}" title="${group.valid} numeric; ${missing} blank/unknown/invalid; ${group.notCollected} not collected. Click to inspect."><span class="coverage-stack"><span style="background:var(--green);width:${100*group.valid/group.n}%"></span><span style="background:var(--amber);width:${100*missing/group.n}%"></span><span class="not-collected" style="width:${100*group.notCollected/group.n}%"></span></span>${fmt(group.valid)} / ${fmt(group.n)}<br><small>${(100*group.valid/group.n).toFixed(1)}% numeric</small></button></td>`;
  }).join('')}</tr>`).join('')}</tbody></table>`;
}
function compareRows(a,b) {
  const av=a[state.sort],bv=b[state.sort];
  if(av==null) return bv==null?0:1; if(bv==null) return -1;
  const comparison=typeof av==='number' && typeof bv==='number'?av-bv:String(av).localeCompare(String(bv),undefined,{numeric:true});
  return comparison*state.direction;
}
function pageRows(rows,key) {
  state[key]=Math.min(state[key],Math.max(0,Math.ceil(rows.length/PAGE)-1));
  return rows.slice(state[key]*PAGE,(state[key]+1)*PAGE);
}
function pagination(id,rows,key) {
  $(id).innerHTML=`<span>${fmt(rows.length)} records${rows.length?' · '+fmt(state[key]*PAGE+1)+'–'+fmt(Math.min((state[key]+1)*PAGE,rows.length)):''}</span><div><button data-page-key="${key}" data-page-delta="-1" ${!state[key]?'disabled':''}>Previous</button><span>Page ${state[key]+1} / ${Math.max(1,Math.ceil(rows.length/PAGE))}</span><button data-page-key="${key}" data-page-delta="1" ${(state[key]+1)*PAGE>=rows.length?'disabled':''}>Next</button></div>`;
}
function renderRecords() {
  visibleRecords.sort(compareRows);
  const fields=[['survey_year','Year'],['program_id','Frame'],['plot_id','Plot'],['source_individual_id','Source ID'],['status','Status'],['height_m','Height (m)'],['arm_count','Arms']];
  $('records-table').innerHTML=visibleRecords.length?`<table><thead><tr><th>Open record</th>${fields.map(([key,title])=>`<th><button class="sort" data-sort="${key}">${title}${state.sort===key?(state.direction===1?' ↑':' ↓'):''}</button></th>`).join('')}<th>Findings</th><th>Identity</th></tr></thead><tbody>${pageRows(visibleRecords,'pageObs').map(row=>`<tr class="selectable" data-entity="${row.observation_id}"><td><button class="textbutton mono" data-entity="${row.observation_id}">${row.observation_id.slice(0,9)}…</button></td><td>${row.survey_year}</td><td>${esc(label(row.program_id))}</td><td>${esc(row.plot_id||'—')}</td><td>${esc(row.source_individual_id||'—')}</td><td>${esc(row.status)}</td><td class="numeric">${fmt(row.height_m)}${row.unit_source==='inferred'?' *':''}</td><td class="numeric">${fmt(row.arm_count)}</td><td class="numeric">${fmt((entityFindings.get(row.observation_id)||[]).length)}</td><td>${row.organism_id?badge('linked','info'):'unlinked'}</td></tr>`).join('')}</tbody></table>`:empty('No records match the selected scope and availability filter.');
  pagination('records-pagination',visibleRecords,'pageObs');
}
function renderFindings() {
  $('findings-table').innerHTML=visibleFindings.length?`<table><thead><tr><th>Severity</th><th>Rule / open evidence</th><th>Frame</th><th>Year</th><th>Plot</th><th>Field</th><th>Observed value</th></tr></thead><tbody>${pageRows(visibleFindings,'pageFind').map(row=>`<tr class="selectable" data-entity="${esc(row.entity_identifier)}" data-fi="${row.index}"><td>${badge(row.severity)}</td><td><button class="textbutton" data-entity="${esc(row.entity_identifier)}" data-fi="${row.index}">${esc(row.rule_id)}</button><br><span class="mono">${esc(row.entity_identifier.slice(0,12))}…</span></td><td>${esc(label(row.program_id))}</td><td>${row.survey_year??'undated'}</td><td>${esc(row.plot_id||'—')}</td><td>${esc(row.field)}</td><td class="mono">${esc(JSON.stringify(row.observed_value).slice(0,160))}</td></tr>`).join('')}</tbody></table>`:empty('No findings match these filters. Try clearing the rule or severity filter.');
  pagination('findings-pagination',visibleFindings,'pageFind');
}
function summaryMatches(row) {
  return (!state.program||row.program_id===state.program)&&(!state.year||String(row.survey_year)===state.year)&&
    (!state.q||[row.observation_id,row.plot_id].join(' ').toLowerCase().includes(state.q.toLowerCase()));
}
function renderSummaries() {
  $('summary-kind').value=state.summaryKind;$('representation').value=state.representation;
  const vegetation=state.summaryKind==='vegetation';$('representation-label').hidden=vegetation;
  visibleSummaries=summaryRows[state.summaryKind].filter(row=>summaryMatches(row)&&
    (vegetation||!state.representation||row.representation===state.representation)&&
    (!state.summaryQ||[row.plot_id,row.species_raw,row.species_name_raw].join(' ').toLowerCase().includes(state.summaryQ.toLowerCase())));
  $('summary-note').textContent=vegetation?'Taxon/plot/round summaries are not individually tracked plants. Count and Stems retain source meaning; cover remains raw because fraction/percent semantics are unresolved. 1990 workbook sheets are empty: historical mapped attributes can be inspected in Sources & schemas.':'Source representations overlap: do not sum their rows as independent samples. The 1990 plot counts are density-derived estimates and may be fractional. Historic/GPS labels inside the Census workbook remain in a separate auxiliary summary namespace; no crosswalk is assumed.';
  const years=tally(visibleSummaries,'survey_year').sort((a,b)=>Number(a[0])-Number(b[0]));
  $('summary-chart').innerHTML=years.length?'<p class="caption">Summary records by source year · click to filter. These bars count rows, not organisms.</p>'+years.map(([year,count])=>barHTML(year,count,Math.max(...years.map(r=>r[1])),'#6e8d55','summary-year',String(year))).join(''):'';
  const fields=vegetation?[['survey_year','Year'],['plot_id','Subplot'],['species_raw','Taxon code'],['species_name_raw','Source name'],['count','Count / stems'],['cover_raw','Raw cover'],['cover_unit_raw','Source cover label'],['area_m2','Area (m²)']]:[['survey_year','Year'],['program_id','Frame'],['plot_id','Plot'],['representation','Representation'],['count_estimate','Count estimate'],['density_per_ha','Density / ha'],['count_basis','Count basis']];
  $('summaries-table').innerHTML=visibleSummaries.length?`<table><thead><tr><th>Open source evidence</th>${fields.map(([,title])=>`<th>${title}</th>`).join('')}</tr></thead><tbody>${pageRows(visibleSummaries,'pageSummary').map(row=>`<tr class="selectable" data-entity="${row.observation_id}"><td><button class="textbutton mono" data-entity="${row.observation_id}">${row.observation_id.slice(0,9)}…</button></td>${fields.map(([key])=>`<td>${key==='program_id'?esc(label(row[key])):typeof row[key]==='number'?fmt(row[key]):esc(row[key]??'—')}</td>`).join('')}</tr>`).join('')}</tbody></table>`:empty('No summary records match this frame, year and representation. Clear the frame/year filters or choose another representation.');
  pagination('summaries-pagination',visibleSummaries,'pageSummary');
}
function setupCanvas(canvas) {
  const rect=canvas.getBoundingClientRect(), dpr=window.devicePixelRatio||1;
  const width=Math.max(100,rect.width),height=Math.max(100,rect.height);
  canvas.width=Math.round(width*dpr); canvas.height=Math.round(height*dpr);
  const ctx=canvas.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0); ctx.clearRect(0,0,width,height);
  return {ctx,width,height};
}
function pairStatus(pair) {
  const matching=(entityFindings.get(pair.after_id)||[]).filter(f=>f.observed_value?.previous===pair.before_id);
  if(state.pairMeasure==='arms') return matching.some(f=>f.rule_id==='TEMPORAL_ARM_DECREASE')?'decrease':'other';
  if(matching.some(f=>f.rule_id==='TEMPORAL_SHRINKAGE'))return 'decrease';
  if(matching.some(f=>f.rule_id==='TEMPORAL_GROWTH_OUTLIER'))return 'growth';
  return 'other';
}
function renderPairs() {
  $('pair-measure').value=state.pairMeasure;$('pair-interval').value=state.pairInterval;
  const isArms=state.pairMeasure==='arms',isGrowth=state.pairMeasure==='growth';
  const xfield=isArms?'arms_before':'height_before',yfield=isArms?'arms_after':isGrowth?'annual_growth_m':'height_after';
  visiblePairs=data.pairs.filter(pair=>recordMatches(obsIndex.get(pair.after_id))&&(!state.pairInterval||`${pair.before_year}–${pair.after_year}`===state.pairInterval)&&present(pair[xfield])&&present(pair[yfield]));
  const {ctx,width,height}=setupCanvas($('pairs'));
  if(!visiblePairs.length){pairsPlot=null;ctx.fillStyle='#64736c';ctx.font='13px system-ui';ctx.fillText('No supported measurement pairs match this selection.',25,70);$('pairs-caption').textContent='Unlinked censuses and missing measurements do not generate individual change pairs.';}
  else {
    const xs=visiblePairs.map(p=>p[xfield]),ys=visiblePairs.map(p=>p[yfield]);
    const max=Math.max(1,...xs,...ys)*1.08;
    const xmin=0,xmax=isGrowth?Math.max(1,...xs)*1.08:max,ymin=isGrowth?Math.min(0,...ys)*1.1:0,ymax=isGrowth?Math.max(.1,...ys)*1.1:max;
    const left=60,right=22,top=20,bottom=52;
    const x=value=>left+(value-xmin)/(xmax-xmin)*(width-left-right),y=value=>height-bottom-(value-ymin)/(ymax-ymin)*(height-top-bottom);
    ctx.font='11px system-ui';ctx.fillStyle='#64736c';ctx.strokeStyle='#dce2d8';ctx.lineWidth=1;
    const ystep=niceStep(ymax-ymin),xstep=niceStep(xmax-xmin);
    for(let value=Math.ceil(ymin/ystep)*ystep;value<=ymax;value+=ystep){ctx.beginPath();ctx.moveTo(left,y(value));ctx.lineTo(width-right,y(value));ctx.stroke();ctx.textAlign='right';ctx.fillText(fmt(value),left-8,y(value)+4);}
    ctx.textAlign='center';for(let value=0;value<=xmax;value+=xstep)ctx.fillText(fmt(value),x(value),height-bottom+18);
    ctx.fillText(isArms?'Arms in prior survey':'Height in prior survey (m)',width/2,height-6);
    ctx.textAlign='left';ctx.fillText(isArms?'Later arms':isGrowth?'Growth (m/year)':'Later height (m)',left,12);
    if(!isGrowth){ctx.setLineDash([5,4]);ctx.strokeStyle='#97a591';ctx.beginPath();ctx.moveTo(x(0),y(0));ctx.lineTo(x(max),y(max));ctx.stroke();ctx.setLineDash([]);}
    const pixels=[];
    // Draw unflagged context first, leaving review candidates visible on top.
    const ordered=[...visiblePairs].sort((a,b)=>(pairStatus(a)==='other'?0:1)-(pairStatus(b)==='other'?0:1));
    for(const pair of ordered){const status=pairStatus(pair),px=x(pair[xfield]),py=y(pair[yfield]);ctx.fillStyle=status==='decrease'?'#ad5546':status==='growth'?'#857196':'#42745b';ctx.globalAlpha=status==='other'?.35:.9;ctx.beginPath();ctx.arc(px,py,status==='other'?2.5:4,0,Math.PI*2);ctx.fill();pixels.push({x:px,y:py,pair,row:obsIndex.get(pair.after_id)});}
    ctx.globalAlpha=1;pairsPlot={points:pixels};
    const flagged=visiblePairs.filter(p=>pairStatus(p)!=='other').length;
    $('pairs-caption').textContent=`${fmt(visiblePairs.length)} eligible linked pairs · ${fmt(flagged)} trigger a measurement-specific temporal screen. Colors refer to this exact prior/later pair; other findings on the same record do not recolor it.`;
  }
  const tableRows=[...visiblePairs].sort((a,b)=>(pairStatus(b)==='other'?0:1)-(pairStatus(a)==='other'?0:1));
  $('pairs-table').innerHTML=tableRows.length?`<table><thead><tr><th>Later record / evidence</th><th>Interval</th><th>Plot / source ID</th><th>Prior ${isArms?'arms':'height (m)'}</th><th>Later ${isArms?'arms':'height (m)'}</th><th>Annual growth (m/year)</th><th>Pair screen</th></tr></thead><tbody>${pageRows(tableRows,'pagePairs').map(pair=>{const row=obsIndex.get(pair.after_id);return `<tr class="selectable" data-entity="${pair.after_id}"><td><button class="textbutton mono" data-entity="${pair.after_id}">${pair.after_id.slice(0,12)}…</button></td><td>${pair.before_year} → ${pair.after_year}</td><td>${esc(row.plot_id)} / ${esc(row.source_individual_id)}</td><td>${fmt(pair[isArms?'arms_before':'height_before'])}</td><td>${fmt(pair[isArms?'arms_after':'height_after'])}</td><td>${fmt(pair.annual_growth_m)}</td><td>${esc(pairStatus(pair))}</td></tr>`;}).join('')}</tbody></table>`:empty('No individual change pairs to list.');
  pagination('pairs-pagination',tableRows,'pagePairs');
}
function niceStep(span,target=6) { const raw=span/target, power=10**Math.floor(Math.log10(raw)); return [1,2,5,10].map(n=>n*power).find(n=>n>=raw)||power*10; }
function drawScatter() {
  const {ctx,width,height}=setupCanvas($('scatter'));
  const points=visibleRecords.filter(row=>present(row[state.measure]));
  const left=55,right=20,top=18,bottom=40;
  if(!points.length) { ctx.fillStyle='#64736c';ctx.font='13px system-ui';ctx.fillText('No numeric measurements in this selection.',30,70);scatterPlot=null; $('scatter-caption').textContent=`${fmt(visibleRecords.length)} records have no numeric value for this measurement. Null is not zero.`;return; }
  const years=points.map(r=>r.survey_year),values=points.map(r=>r[state.measure]);
  const domain=scatterBounds||[Math.min(...years)-1,Math.max(...years)+1,Math.min(0,Math.min(...values)),Math.max(1,Math.max(...values)*1.05)];
  const [xmin,xmax,ymin,ymax]=domain;
  const x=value=>left+(value-xmin)/(xmax-xmin)*(width-left-right), y=value=>height-bottom-(value-ymin)/(ymax-ymin)*(height-top-bottom);
  ctx.font='11px system-ui';ctx.fillStyle='#64736c';ctx.strokeStyle='#dce2d8';ctx.lineWidth=1;
  const step=niceStep(ymax-ymin);
  for(let value=Math.ceil(ymin/step)*step;value<=ymax;value+=step) {ctx.beginPath();ctx.moveTo(left,y(value));ctx.lineTo(width-right,y(value));ctx.stroke();ctx.textAlign='right';ctx.fillText(fmt(value),left-9,y(value)+4);}
  let uniqueYears=[...new Set(years)].sort((a,b)=>a-b).filter(v=>v>=xmin&&v<=xmax);
  if(uniqueYears.length>12) uniqueYears=uniqueYears.filter((_,i)=>i%Math.ceil(uniqueYears.length/12)===0);
  ctx.textAlign='center';uniqueYears.forEach(year=>ctx.fillText(String(year),x(year),height-14));
  const pixels=[];ctx.save();ctx.beginPath();ctx.rect(left,top,width-left-right,height-top-bottom);ctx.clip();
  for(const row of points) {
    const jitter=(parseInt(row.observation_id.slice(-4),16)/65535-.5)*.5;
    const px=x(row.survey_year+jitter),py=y(row[state.measure]);
    if(px<left||px>width-right||py<top||py>height-bottom) continue;
    ctx.globalAlpha=.48;ctx.fillStyle=colors[row.program_id]||'#42745b';ctx.beginPath();ctx.arc(px,py,2.1,0,Math.PI*2);ctx.fill();pixels.push({x:px,y:py,row});
  }
  ctx.restore();ctx.globalAlpha=1;
  scatterPlot={points:pixels,domain,left,right:width-right,top,bottom:height-bottom,width,height};
  $('scatter-caption').innerHTML=`${fmt(points.length)} numeric values; ${fmt(visibleRecords.length-points.length)} missing/not collected and absent from the plot. ${fmt(pixels.length)} dots in the current zoom. ${state.measure==='height_m'?'* Historic height units are inferred; zero values remain visible.':''} Source year 2001 in Historic Plots labels the 2001–2002 round. <button class="textbutton" id="scatter-reset">Reset zoom</button>`;
}
function nearest(points,x,y,radius=9) {
  let best=null,distance=radius*radius;
  for(const point of points) { const d=(point.x-x)**2+(point.y-y)**2;if(d<=distance) {best=point;distance=d;} }
  return best;
}
function pointPosition(event,canvas) {const rect=canvas.getBoundingClientRect();return [event.clientX-rect.left,event.clientY-rect.top];}
function pointTooltip(id,point,x,y,canvas,extra='') {
  const tip=$(id);if(!point){tip.hidden=true;return;}
  const row=point.row;
  tip.innerHTML=`<strong>${esc(label(row.program_id))} · ${row.survey_year}</strong><br>${esc(row.plot_id||'No plot')} · source ID ${esc(row.source_individual_id||'—')}<br>Height ${fmt(row.height_m)} m · arms ${fmt(row.arm_count)}<br>${fmt((entityFindings.get(row.observation_id)||[]).length)} findings · click for evidence${extra}`;
  tip.style.left=Math.min(x+14,Math.max(0,canvas.clientWidth-280))+'px';tip.style.top=Math.max(0,Math.min(y+14,canvas.clientHeight-130))+'px';tip.hidden=false;
}
function geoRing(shape,visit) {
  if(shape.type==='Polygon') shape.coordinates.forEach(visit);
  else if(shape.type==='MultiPolygon') shape.coordinates.forEach(polygon=>polygon.forEach(visit));
}
function fitMap(points) {
  if(!points.length) return [-111.3,-110.45,32.03,32.4];
  let xmin=Infinity,xmax=-Infinity,ymin=Infinity,ymax=-Infinity;
  for(const row of points) {xmin=Math.min(xmin,row.longitude);xmax=Math.max(xmax,row.longitude);ymin=Math.min(ymin,row.latitude);ymax=Math.max(ymax,row.latitude);}
  const xp=Math.max(.001,(xmax-xmin)*.08),yp=Math.max(.001,(ymax-ymin)*.08);
  return [xmin-xp,xmax+xp,ymin-yp,ymax+yp];
}
function worstSeverity(row) {
  const list=entityFindings.get(row.observation_id)||[];
  return list.some(f=>f.severity==='error')?'error':list.some(f=>f.severity==='warning')?'warning':list.length?'info':'none';
}
function indexHistoryCoverage() {
  const rounds=new Map();
  for(const row of observations) {
    if(!rounds.has(row.program_id))rounds.set(row.program_id,new Set());
    rounds.get(row.program_id).add(row.survey_year);
  }
  historyCoverage.clear();
  for(const [organism,rows] of organismIndex) {
    const years=[...new Set(rows.map(row=>row.survey_year))].sort((a,b)=>a-b);
    const expected=[...rounds.get(rows[0].program_id)].sort((a,b)=>a-b);
    const missing=expected.filter(year=>!years.includes(year));
    const kind=missing.length===0?'full':years.length<=2?'short':'partial';
    historyCoverage.set(organism,{kind,count:years.length,total:expected.length,years,missing});
  }
}
function mapHistoryInfo(row) {
  return historyCoverage.get(row.organism_id)||{kind:'unlinked',count:null,total:null,years:[],missing:[]};
}
function mapHistoryText(row) {
  const history=mapHistoryInfo(row);
  if(history.kind==='unlinked')return 'Individual history unknown: no supported cross-survey linkage.';
  return `${history.count}/${history.total} survey rounds · ${historyNames[history.kind]}<br>Present: ${history.years.join(', ')}${history.missing.length?'<br>Missing rounds: '+history.missing.join(', '):''}`;
}
function historySymbol(count) {
  const color=historyShade({count});
  return `<svg width="18" height="20" viewBox="-1 -2 18 20" aria-hidden="true"><path d="${cactusOutline}" fill="${count===null?'none':color}" stroke="${count===null?color:'#52724e'}" stroke-width=".8"/></svg>`;
}
function drawMap() {
  ensureMapContext();
  const {ctx,width,height}=setupCanvas($('map'));
  const geocoded=baseRecords.filter(r=>present(r.latitude)&&present(r.longitude));
  // One marker per supported individual; co-location never creates identity.
  const markerIndex=new Map();
  for(const row of geocoded){
    const key=row.organism_id||row.observation_id;
    const previous=markerIndex.get(key);
    if(!previous||row.survey_year>previous.row.survey_year)markerIndex.set(key,{row,coverage:mapHistoryInfo(row)});
  }
  const markers=[...markerIndex.values()];
  const points=markers.map(marker=>marker.row);
  if(!mapBounds) mapBounds=state.mapView==='region'?[-111.32,-110.43,31.98,32.45]:fitMap(points);
  const [xmin,xmax,ymin,ymax]=mapBounds;
  const xScale=Math.min((width-50)/((xmax-xmin)*Math.cos(32.2*Math.PI/180)),(height-50)/(ymax-ymin));
  const sx=xScale*Math.cos(32.2*Math.PI/180),sy=xScale;
  const cx=(xmin+xmax)/2,cy=(ymin+ymax)/2;
  const x=lon=>width/2+(lon-cx)*sx,y=lat=>height/2-(lat-cy)*sy;
  drawMapBackground(ctx,x,y,width,height,sx,sy,cx,cy);
  drawMapContext(ctx,x,y,width,height,sx);
  ctx.font='10px system-ui';ctx.strokeStyle='#dce3d5';ctx.fillStyle='#849180';ctx.lineWidth=1;
  const lonStep=niceStep((width/sx),7),latStep=niceStep(height/sy,6);
  for(let lon=Math.ceil((cx-width/2/sx)/lonStep)*lonStep;lon<cx+width/2/sx;lon+=lonStep) {ctx.beginPath();ctx.moveTo(x(lon),0);ctx.lineTo(x(lon),height);ctx.stroke();ctx.fillText(lon.toFixed(3)+'°',x(lon)+4,14);}
  for(let lat=Math.ceil((cy-height/2/sy)/latStep)*latStep;lat<cy+height/2/sy;lat+=latStep) {ctx.beginPath();ctx.moveTo(0,y(lat));ctx.lineTo(width,y(lat));ctx.stroke();ctx.fillText(lat.toFixed(3)+'°',5,y(lat)-5);}
  for(const feature of data.plots.features) {
    if(!mapLayers.plots)continue;
    if(state.program && feature.properties.program_id!==state.program) continue;
    ctx.beginPath();geoRing(feature.geometry,ring=>{ring.forEach((coord,i)=>i?ctx.lineTo(x(coord[0]),y(coord[1])):ctx.moveTo(x(coord[0]),y(coord[1])));ctx.closePath();});
    ctx.fillStyle='#d8e4d433';ctx.fill('evenodd');ctx.strokeStyle='#839779';ctx.stroke();
  }
  const pixels=[];
  const order={unlinked:0,full:1,partial:2,short:3};
  const ordered=[...markers].sort((a,b)=>order[a.coverage.kind]-order[b.coverage.kind]);
  for(const {row,coverage} of ordered) {
    const px=x(row.longitude),py=y(row.latitude);if(px<0||px>width||py<0||py>height) continue;
    const color=$('map-color').value==='history'?historyShade(coverage):$('map-color').value==='finding'?severityColors[worstSeverity(row)]:(colors[row.program_id]||'#42745b');
    const complete=coverage.kind==='full';
    ctx.save();ctx.translate(px-8,py-8);
    ctx.strokeStyle='#fffefa';ctx.lineWidth=2.4;ctx.stroke(cactusPath);
    ctx.fillStyle=color;
    if(coverage.count!==null)ctx.fill(cactusPath);
    ctx.strokeStyle=coverage.count===null?color:$('map-color').value==='history'?'#52724e':color;
    ctx.lineWidth=coverage.count===null?1.2:.65;ctx.stroke(cactusPath);ctx.restore();
    pixels.push({x:px,y:py,row,complete,coverage,color,marker:'cactus'});
  }
  ctx.globalAlpha=1;mapPlot={points:pixels,sx,sy,width,height};
  const linked=markers.filter(marker=>marker.row.organism_id).length;
  $('map-caption').textContent=`${fmt(geocoded.length)} / ${fmt(baseRecords.length)} selected observations have geographic coordinates. Shown as ${fmt(linked)} linked cacti plus ${fmt(markers.length-linked)} unlinked observations; ${fmt(pixels.length)} markers are in the viewport. Each linked cactus appears once at its latest visible location. Unknown-CRS source features are not positioned on this map.`;
  $('map-legend').innerHTML=$('map-color').value==='history'?'':$('map-color').value==='finding'?Object.entries(severityColors).map(([key,color])=>`<span><i style="background:${color}"></i>${key==='none'?'No finding':key}</span>`).join(''):[...new Set(points.map(r=>r.program_id))].map(program=>`<span><i style="background:${colors[program]}"></i>${esc(label(program))}</span>`).join('');
  let availabilityLegend=$('map-completeness-legend');
  if(!availabilityLegend){availabilityLegend=document.createElement('div');availabilityLegend.id='map-completeness-legend';$('map-legend').before(availabilityLegend);}
  availabilityLegend.innerHTML=`<div class="legend">${[1,2,3,4,null].map(count=>`<span>${historySymbol(count)}${count===null?'History unknown':count+' survey round'+(count===1?'':'s')+(count===4?' · all rounds':'')}: ${fmt(markers.filter(marker=>marker.coverage.count===count).length)}</span>`).join('')}</div><p class="caption">With Survey observation count selected, darker green means more distinct survey rounds: 1 (lightest) to 4 (darkest). Hollow gray cacti have unknown individual continuity, including 71G and Section 17. Counts use the complete linked history, regardless of the page's year filter. Historic Plots has four available rounds: 1975, 2001–2002 (source label 2001), 2010 and 2014. Missing years do not imply death. Sampling-frame and finding colors can be selected instead. Hover for exact counts and years.</p>`;
}
function zoomMap(factor,position=null) {
  if(!mapPlot||!mapBounds) return;
  const [xmin,xmax,ymin,ymax]=mapBounds,cx=(xmin+xmax)/2,cy=(ymin+ymax)/2;
  const [px,py]=position||[mapPlot.width/2,mapPlot.height/2];
  const lon=cx+(px-mapPlot.width/2)/mapPlot.sx,lat=cy-(py-mapPlot.height/2)/mapPlot.sy;
  mapBounds=[lon+(xmin-lon)*factor,lon+(xmax-lon)*factor,lat+(ymin-lat)*factor,lat+(ymax-lat)*factor];drawMap();
}
async function ensureSources() {
  if(sources) return sources;
  if(!sourcesPromise) sourcesPromise=fetch('explorer/sources.json').then(response=>{if(!response.ok) throw new Error('Source profiles could not be loaded.');return response.json();}).then(value=>sources=value).catch(error=>{sourcesPromise=null;throw error;});
  return sourcesPromise;
}
function inventoryMatches(row) {
  const dataset=state.program?.startsWith('census_')?'census':state.program;
  return (!dataset||row.dataset===dataset)&&(!state.sourceQ||[row.file,row.sheet].join(' ').toLowerCase().includes(state.sourceQ.toLowerCase()));
}
async function renderSources() {
  $('source-status').textContent=sources?'':'Loading full column profiles…';
  try {await ensureSources();} catch(error) {$('source-status').textContent=error.message;return;}
  if(state.tab!=='sources')return;
  $('source-status').textContent='';
  visibleSources=sources.inventory.map((row,index)=>({...row,index})).filter(inventoryMatches);
  $('sources-table').innerHTML=visibleSources.length?`<table><thead><tr><th>Dataset</th><th>File</th><th>Sheet / layer</th><th>Parsed rows</th><th>Columns</th><th>CRS</th></tr></thead><tbody>${pageRows(visibleSources,'pageSource').map(row=>`<tr class="selectable" data-source="${row.index}"><td>${esc(label(row.dataset))}</td><td>${esc(row.file.split('/').pop())}</td><td><button class="textbutton" data-source="${row.index}">${esc(row.sheet)}</button></td><td class="numeric">${fmt(row.rows)}</td><td class="numeric">${fmt(row.columns)}</td><td>${esc(row.crs||'not declared')}</td></tr>`).join('')}</tbody></table>`:empty('No source sheets or layers match these filters.');
  pagination('sources-pagination',visibleSources,'pageSource');
  const dataset=state.program?.startsWith('census_')?'census':state.program;
  $('schema-cards').innerHTML=sources.schemas.filter(row=>!dataset||row.program_id===dataset).map(row=>`<details class="schema-card"><summary>${esc(label(row.program_id))} · ${esc(row.before)} → ${esc(row.after)}</summary><dl>${Object.entries(row).filter(([key])=>!['program_id','before','after'].includes(key)).map(([key,value])=>`<dt>${esc(key.replaceAll('_',' '))}</dt><dd>${esc(typeof value==='string'?value:pretty(value))}</dd>`).join('')}</dl></details>`).join('')||empty('No explicit schema-change comparison is available for this frame.');
  $('file-cards').innerHTML=data.files.filter(row=>!dataset||row.dataset===dataset).map(row=>`<article class="file-card"><strong>${esc(row.filename)}</strong>${esc(label(row.dataset))} · ${fmt(row.byte_size/1024)} KiB · reference ${esc(row.source_reference_id)}<br><code>SHA-256 ${esc(row.sha256)}</code><br><a href="${esc(row.source_url)}" target="_blank" rel="noopener">NPS record ↗</a><a href="${esc(row.direct_download_url)}" target="_blank" rel="noopener">Official download ↗</a></article>`).join('');
}
async function loadDetail(entity) {
  const prefix=entity.slice(0,2);
  if(!/^[a-f0-9]{24}$/.test(entity)) throw new Error('This entity has no exported source-evidence record.');
  if(!shardCache.has(prefix)) shardCache.set(prefix,fetch(`explorer/details/${prefix}.json`).then(response=>{if(!response.ok)throw new Error('Evidence file could not be loaded.');return response.json();}).catch(error=>{shardCache.delete(prefix);throw error;}));
  const shard=await shardCache.get(prefix);
  if(!shard[entity]) throw new Error('No source evidence was exported for this entity.');
  return shard[entity];
}
async function openEntity(entity,fi='') {
  const token=++detailToken;state.entity=entity;state.fi=String(fi);syncHash();
  $('detail-kicker').textContent='SOURCE EVIDENCE';$('detail-title').textContent='Loading record…';
  $('detail-actions').innerHTML='';$('detail-body').innerHTML='<div class="empty">Fetching full source lineage…</div>';
  if(!$('detail').open)$('detail').showModal();
  try {const detail=await loadDetail(entity);if(token!==detailToken)return;selectedDetail=detail;renderDetail(detail);}
  catch(error) {if(token===detailToken){$('detail-title').textContent='Evidence unavailable';$('detail-body').innerHTML=empty(error.message+' Confirm that this report is being served over HTTP.');}}
}
function sourceBox(row) {
  const file=data.files.find(file=>file.local_filename===row.source_file);
  const url=file?.source_url||`https://irma.nps.gov/DataStore/Reference/Profile/${encodeURIComponent(row.source_reference_id||'')}`;
  return `<div class="source-box"><strong>${esc(row.source_file?.split('/').pop()||'Source artifact')}</strong><br>${esc(row.source_sheet||'')} · ${row.source_dataset==='vegetation'&&row.feature_index!=null?'feature':'row'} ${fmt(row.source_row)} · NPS ${esc(row.source_reference_id||'—')}<p class="mono">${esc(row.source_file||'')}</p><code>SHA-256 ${esc(row.source_sha256||'—')}</code><p><a href="${esc(url)}" target="_blank" rel="noopener">Official NPS record ↗</a>${file?`<a href="${esc(file.direct_download_url)}" target="_blank" rel="noopener">Official source download ↗</a>`:''}<button class="textbutton" data-profile-file="${esc(row.source_file||'')}" data-profile-sheet="${esc(row.source_sheet||'')}">Inspect this sheet/layer profile →</button></p></div>`;
}
function historyHTML(row) {
  const history=row.organism_id?organismIndex.get(row.organism_id)||[]:[];
  if(!row.organism_id) {
    const explanation=row.program_id==='historic_plots'&&row.source_plot_id==='71G'?'Individual linkage is withheld on 71G because the original report documents tag loss.':row.program_id?.startsWith('census')?'Source cactus numbers have no verified cross-round identity. Repeated plot sampling is not an individual history.':'No supported longitudinal individual identifier is available for this record.';
    return `<h3>Individual history</h3><p class="caption">${esc(explanation)}</p>`;
  }
  const rows=[...history].sort((a,b)=>a.survey_year-b.survey_year);
  const years=rows.map(r=>r.survey_year),valid=rows.filter(r=>present(r.height_m));
  const xmin=Math.min(...years)-1,xmax=Math.max(...years)+1,ymax=Math.max(1,...valid.map(r=>r.height_m))*1.12;
  const x=year=>55+(year-xmin)/(xmax-xmin)*870,y=height=>180-height/ymax*150;
  let marks='',lines='';
  const yearCounts=new Map();rows.forEach(r=>yearCounts.set(r.survey_year,(yearCounts.get(r.survey_year)||0)+1));
  for(let i=0;i<rows.length;i++) {
    const current=rows[i],previous=rows[i-1];
    if(previous && previous.height_m>0 && current.height_m>0 && yearCounts.get(previous.survey_year)===1 && yearCounts.get(current.survey_year)===1) lines+=`<line x1="${x(previous.survey_year)}" y1="${y(previous.height_m)}" x2="${x(current.survey_year)}" y2="${y(current.height_m)}" stroke="#8ca48d" stroke-width="2"/>`;
    if(present(current.height_m))marks+=`<circle class="history-point" role="button" tabindex="0" aria-label="Open ${current.survey_year} record, height ${current.height_m} meters" data-entity="${current.observation_id}" cx="${x(current.survey_year)}" cy="${y(current.height_m)}" r="${current.observation_id===row.observation_id?7:5}" fill="${current.height_m===0?'#fffefa':colors[current.program_id]}" stroke="${current.height_m===0?'#c79435':'#42745b'}" stroke-width="2"><title>${current.survey_year}: ${current.height_m} m; ${current.status}</title></circle>`;
  }
  return `<h3>Source-supported individual history</h3><p class="caption">Full history is shown regardless of the page's year filter. Hollow amber points are unresolved zero heights. Lines break at null/zero endpoints and ambiguous duplicate years. Height units are inferred for Historic Plots; 2001 labels the 2001–2002 round.</p><svg class="history-chart" viewBox="0 0 960 220" role="img" aria-label="Individual height history; select records in the table below"><line x1="55" y1="180" x2="925" y2="180" stroke="#dce2d8"/><text x="8" y="28" font-size="12" fill="#64736c">Height (m)</text>${[0,ymax/2,ymax].map(v=>`<text x="45" y="${y(v)+4}" text-anchor="end" font-size="11" fill="#64736c">${fmt(v)}</text>`).join('')}${[...new Set(years)].map(year=>`<text x="${x(year)}" y="205" text-anchor="middle" font-size="11" fill="#64736c">${year}</text>`).join('')}${lines}${marks}</svg><div class="scroll"><table><thead><tr><th>Open year</th><th>Height (m)</th><th>Arms</th><th>Status</th><th>Height availability</th><th>Findings</th></tr></thead><tbody>${rows.map(item=>`<tr class="selectable" data-entity="${item.observation_id}"><td><button class="textbutton" data-entity="${item.observation_id}">${item.survey_year}${item.observation_id===row.observation_id?' · selected':''}</button></td><td>${fmt(item.height_m)}</td><td>${fmt(item.arm_count)}</td><td>${esc(item.status)}</td><td>${esc(item.height_missing_reason||'numeric')}${item.height_m===0?' · zero unresolved':''}</td><td>${(entityFindings.get(item.observation_id)||[]).length}</td></tr>`).join('')}</tbody></table></div>`;
}
function renderDetail(detail) {
  const row=detail.canonical;
  const isObservation=detail.kind==='observation';
  $('detail-kicker').textContent=isObservation?'OBSERVATION → SOURCE':detail.kind.replaceAll('_',' ').toUpperCase();
  $('detail-title').textContent=isObservation?`${label(row.program_id)} · ${row.plot_id||'no plot'} · ${row.survey_year}`:(row.layer||row.representation||'Source record');
  $('detail-actions').innerHTML='<button id="detail-share">Copy record link</button><button id="detail-export">Export full evidence JSON</button>';
  let facts=isObservation?[
    ['Height',row.height_m==null?`— (${row.height_missing_reason||'missing'})`:`${fmt(row.height_m)} m${row.unit_source==='inferred'?' · unit inferred':''}`],
    ['Arm count',row.arm_count==null?`— (${row.arm_count_missing_reason||'missing'})`:fmt(row.arm_count)],
    ['Status',`${row.status} · ${row.status_source}`],['Identity',row.organism_id?'Source-supported individual':(row.source_plot_id==='71G'?'Linkage withheld on 71G':'Unlinked observation')]
  ]:[['Layer / representation',row.layer||row.representation||'—'],['CRS',row.crs||'not documented'],['Source row / feature',fmt(row.source_row)],['Review findings',detail.findings.length]];
  if(detail.kind==='vegetation_observations') {
    $('detail-title').textContent=`Vegetation · ${row.plot_id} · ${row.survey_year} · ${row.species_raw}`;
    facts=[['Source taxon',row.species_name_raw||row.species_raw],['Count / stems',fmt(row.count)],['Raw cover',`${row.cover_raw||'blank'} · label ${row.cover_unit_raw}`],['Area',row.area_m2==null?'not recorded':`${fmt(row.area_m2)} m²`]];
  } else if(detail.kind==='plot_observations') {
    $('detail-title').textContent=`Plot summary · ${row.plot_id} · ${row.survey_year}`;
    facts=[['Count estimate',fmt(row.count_estimate)],['Density / ha',fmt(row.density_per_ha)],['Count basis',row.count_basis],['Representation',row.representation]];
  }
  const selectedFinding=detail.findings.find(item=>String(item.finding_index)===state.fi);
  const ordered=selectedFinding?[selectedFinding,...detail.findings.filter(item=>item!==selectedFinding)]:detail.findings;
  const findingsHTML=ordered.map(item=>{
    const previous=item.observed_value?.previous||item.observed_value?.previous_observation_id;
    return `<article class="finding-card ${esc(item.severity)} ${item===selectedFinding?'active':''}"><h3>${badge(item.severity)} ${esc(item.rule_id)} · ${badge(item.status)}</h3><p>${esc(item.message)}</p><p><strong>Expected:</strong> ${esc(item.expected_condition)}</p><pre>${esc(pretty(item.observed_value))}</pre><button data-lineage-finding="${esc(item.finding_id)}">Trace finding evidence</button>${previous?`<button class="textbutton" data-entity="${esc(previous)}">Open the prior observation →</button>`:''}</article>`;
  }).join('')||'<p class="caption">No validation finding is recorded for this entity. This is not evidence that every possible check was applicable.</p>';
  const highlight=new Set(detail.transforms.filter(t=>!selectedFinding||selectedFinding.field.split(',').includes(t.field)).map(t=>t.source_column));
  const sourceField=selectedFinding?.field||'';
  const rawHTML=`<div class="scroll"><table><thead><tr><th>Original field</th><th>Source value</th></tr></thead><tbody>${Object.entries(detail.raw||{}).map(([key,value])=>`<tr class="${highlight.has(key)||key===sourceField?'raw-highlight':''}"><td>${esc(key)}</td><td>${value===''?'<span class="caption">(blank string)</span>':value===null?'<span class="caption">(null)</span>':esc(typeof value==='object'?pretty(value):value)}</td></tr>`).join('')}</tbody></table></div>`;
  const transformsHTML=detail.transforms.length?`<div class="scroll"><table><thead><tr><th>Canonical field</th><th>Source field</th><th>Source value</th><th>Normalized value</th><th>Transformation</th><th>Value kind</th></tr></thead><tbody>${detail.transforms.map(t=>`<tr><td>${esc(t.field)}</td><td>${esc(t.source_column||'not collected')}</td><td>${t.source_value===''?'(blank)':esc(t.source_value??'null')}</td><td>${esc(t.normalized_value??'null')}</td><td class="mono">${esc(t.transformation)}</td><td>${badge(t.value_kind,t.value_kind)}</td></tr>`).join('')}</tbody></table></div>`:empty('No field-normalization trace is recorded for this source representation. Raw attributes and file lineage remain available.');
  $('detail-body').innerHTML=`<div class="record-facts">${facts.map(([title,value])=>`<div class="record-fact"><small>${esc(title)}</small>${esc(value)}</div>`).join('')}</div>${photoEvidenceHTML(detail)}<h3>Review findings (${detail.findings.length})</h3>${findingsHTML}${isObservation?historyHTML(row):''}${lineagePanel(detail)}<h3>Source lineage</h3>${sourceBox(row)}<div class="detail-tabs" role="tablist" aria-label="Evidence views"><button data-detail-tab="raw" aria-selected="true" role="tab">Raw source values</button><button data-detail-tab="transforms" aria-selected="false" role="tab">Transformations</button><button data-detail-tab="canonical" aria-selected="false" role="tab">Canonical record</button></div><div data-detail-panel="raw">${rawHTML}</div><div data-detail-panel="transforms" hidden>${transformsHTML}</div><div data-detail-panel="canonical" hidden><pre class="raw-json">${esc(pretty(row))}</pre></div>`;
}
async function openSource(index) {
  await ensureSources();const row=sources.inventory[index];if(!row)return;
  state.entity='';state.fi='';syncHash();selectedDetail=null;
  $('detail-kicker').textContent='ORIGINAL SCHEMA & MISSINGNESS';$('detail-title').textContent=row.sheet;
  $('detail-actions').innerHTML='';
  const file=data.files.find(item=>item.local_filename===row.file);
  $('detail-body').innerHTML=`<p class="caption">${esc(row.file.split('/').pop())} · ${esc(label(row.dataset))} · ${fmt(row.rows)} parsed rows · header at ${row.header_row==null?'not applicable':'Excel row '+row.header_row}. Blank counts measure empty/null cells; literal NA, dead, and not measured remain distinct values.</p>${file?sourceBox({source_file:row.file,source_sheet:row.sheet,source_row:row.header_row,source_reference_id:row.source_reference_id,source_sha256:row.sha256}):''}<h3>Column profiles</h3><div class="scroll"><table><thead><tr><th>Parsed field</th><th>Original header</th><th>Inferred type</th><th>Blank/null</th><th>Distinct populated values</th><th>Literal categories</th></tr></thead><tbody>${row.fields.map((field,i)=>`<tr><td>${esc(field.name)}</td><td>${esc(row.original_columns?.[i]??field.name)}</td><td>${esc(field.dtype)}</td><td>${fmt(field.missing_count)} / ${fmt(row.rows)}<br>${field.missing_fraction==null?'—':(field.missing_fraction*100).toFixed(1)+'%'}</td><td>${fmt(field.unique_count)}</td><td>${field.categories?`<details><summary>${Object.keys(field.categories).length} values</summary>${Object.entries(field.categories).map(([key,count])=>`<div><code>${esc(key)}</code>: ${fmt(count)}</div>`).join('')}</details>`:'not a small-category field'}</td></tr>`).join('')}</tbody></table></div><h3>Candidate identifiers</h3><p class="mono">${esc(pretty(row.candidate_id_fields))}</p><p class="caption">Candidate fields are hints from column names, not proof of stable individual identity. Sheet and layer counts may include duplicated representations or source summaries.</p>`;
  if(!$('detail').open)$('detail').showModal();
}
function downloadText(content,name,type) {
  const url=URL.createObjectURL(new Blob([content],{type})),anchor=document.createElement('a');anchor.href=url;anchor.download=name;anchor.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
function csv(rows,columns,name) {
  const cell=value=>{const text=value==null?'':typeof value==='object'?JSON.stringify(value):String(value);return '"'+text.replaceAll('"','""')+'"';};
  downloadText([columns.map(cell).join(','),...rows.map(row=>columns.map(key=>cell(row[key])).join(','))].join('\r\n'),name,'text/csv;charset=utf-8');toast(`Exported ${fmt(rows.length)} rows.`);
}
function attachEvents() {
  $('photo-search').oninput=event=>{state.photoQ=event.target.value;state.pagePhotos=0;renderPhotos();};
  $('photo-license').onchange=event=>{state.photoLicense=event.target.value;state.pagePhotos=0;renderPhotos();};
  $('export-photo-links').onclick=()=>csv(visiblePhotos,['observation_id','photo_id','observation_url','photo_page_url','image_url','license','attribution'],'saguarodata-photo-links.csv');
  $('program').onchange=event=>updateScope({program:event.target.value});
  $('year').onchange=event=>updateScope({year:event.target.value});
  let searchTimer;$('search').oninput=event=>{clearTimeout(searchTimer);const value=event.target.value;searchTimer=setTimeout(()=>updateScope({q:value}),180);};
  $('reset').onclick=()=>{Object.assign(state,{program:'',year:'',q:'',rule:'',severity:'',mode:'all',sourceQ:'',summaryQ:'',pairInterval:'',representation:'RawData_1990_Total_Saguaros'});$('source-search').value='';$('summary-search').value='';updateScope({});};
  $('share').onclick=copyLink;$('all-findings').onclick=()=>{state.rule='';state.severity='';setTab('findings');};
  $('coverage-field').onchange=event=>{state.coverageField=event.target.value;renderCoverage();};
  $('measure').onchange=event=>{state.measure=event.target.value;scatterBounds=null;drawScatter();};
  $('record-mode').onchange=event=>{state.mode=event.target.value;state.pageObs=0;scatterBounds=null;render();};
  for(const key of ['rule','severity'])$(key).onchange=event=>{state[key]=event.target.value;state.pageFind=0;render();};
  $('clear-finding-filters').onclick=()=>{state.rule='';state.severity='';state.pageFind=0;render();};
  $('export-records').onclick=()=>csv(visibleRecords,data.observation_columns,'saguarodata-observations.csv');
  $('export-findings').onclick=()=>csv(visibleFindings,data.finding_columns,'saguarodata-findings.csv');
  $('source-search').oninput=event=>{state.sourceQ=event.target.value;state.pageSource=0;renderSources();};
  $('pair-measure').onchange=event=>{state.pairMeasure=event.target.value;state.pagePairs=0;syncHash();renderPairs();};
  $('pair-interval').onchange=event=>{state.pairInterval=event.target.value;state.pagePairs=0;syncHash();renderPairs();};
  $('summary-kind').onchange=event=>{state.summaryKind=event.target.value;state.pageSummary=0;syncHash();renderSummaries();};
  $('representation').onchange=event=>{state.representation=event.target.value;state.pageSummary=0;syncHash();renderSummaries();};
  $('summary-search').oninput=event=>{state.summaryQ=event.target.value;state.pageSummary=0;renderSummaries();};
  $('export-summaries').onclick=()=>csv(visibleSummaries,data.summary_columns[state.summaryKind],'saguarodata-'+state.summaryKind+'-summaries.csv');
  $('export-pairs').onclick=()=>csv(visiblePairs,['before_id','after_id','program_id','before_year','after_year','height_before','height_after','annual_growth_m','arms_before','arms_after'],'saguarodata-linked-pairs.csv');
  $('map-color').onchange=drawMap;$('map-in').onclick=()=>zoomMap(.65);$('map-out').onclick=()=>zoomMap(1.5);$('map-reset').onclick=()=>{state.mapView='records';syncHash();mapBounds=null;drawMap();};
  $('map-region').onclick=()=>{state.mapView='region';syncHash();mapBounds=null;drawMap();};
  $('map-background').onchange=()=>{state.mapBackground=$('map-background').value;syncHash();drawMap();};
  document.querySelectorAll('[data-map-layer]').forEach(input=>input.onchange=()=>{mapLayers[input.dataset.mapLayer]=input.checked;drawMap();});
  $('close-detail').onclick=()=>$('detail').close();
  $('detail').addEventListener('close',()=>{if($('detail').open)return;detailToken++;state.entity='';state.fi='';syncHash();});
  document.addEventListener('click',event=>{
    const target=event.target.closest('button,[data-entity], [data-source]');if(!target)return;
    if(target.dataset.lineageFinding){showLineage(target.dataset.lineageFinding);return;}
    if(target.id==='lineage-observation'){showLineage();return;}
    if(target.id==='lineage-download'&&activeLineage){downloadText(pretty(activeLineage),'saguarodata-lineage-trace.json','application/json');return;}
    if(target.dataset.photoBrowse){$('detail').close();setTab('photos');return;}
    if(target.dataset.tab){if(target.dataset.summaryKind){state.summaryKind=target.dataset.summaryKind;state.representation='';state.pageSummary=0;}setTab(target.dataset.tab);return;}
    if(target.dataset.programPick){updateScope({program:state.program===target.dataset.programPick?'':target.dataset.programPick});return;}
    if(target.dataset.rulePick){state.rule=target.dataset.rulePick;state.severity='';state.pageFind=0;setTab('findings');return;}
    if(target.dataset.cellProgram){Object.assign(state,{program:target.dataset.cellProgram,year:target.dataset.cellYear,tab:'records',mode:'all',measure:state.coverageField});updateScope({});return;}
    if(target.dataset.sort){state.direction=state.sort===target.dataset.sort?-state.direction:1;state.sort=target.dataset.sort;state.pageObs=0;renderRecords();return;}
    if(target.dataset.pageKey){state[target.dataset.pageKey]+=Number(target.dataset.pageDelta);if(state.tab==='sources')renderSources();else if(state.tab==='findings')renderFindings();else if(state.tab==='changes')renderPairs();else if(state.tab==='summaries')renderSummaries();else if(state.tab==='photos')renderPhotos();else renderRecords();return;}
    if(target.dataset.summaryYear){updateScope({year:target.dataset.summaryYear});return;}
    if(target.dataset.entity){openEntity(target.dataset.entity,target.dataset.fi??'');return;}
    if(target.dataset.source!==undefined){openSource(Number(target.dataset.source));return;}
    if(target.dataset.detailTab){document.querySelectorAll('[data-detail-tab]').forEach(button=>button.setAttribute('aria-selected',String(button.dataset.detailTab===target.dataset.detailTab)));document.querySelectorAll('[data-detail-panel]').forEach(panel=>panel.hidden=panel.dataset.detailPanel!==target.dataset.detailTab);return;}
    if(target.dataset.profileFile!==undefined){ensureSources().then(()=>{const index=sources.inventory.findIndex(row=>row.file===target.dataset.profileFile&&row.sheet===target.dataset.profileSheet);if(index>=0)openSource(index);else toast('No sheet profile is available for this artifact.');});return;}
    if(target.id==='scatter-reset'){scatterBounds=null;drawScatter();return;}
    if(target.id==='detail-share'){copyLink();return;}
    if(target.id==='detail-export'&&selectedDetail)downloadText(pretty(selectedDetail),'saguarodata-'+state.entity+'.json','application/json');
  });
  document.addEventListener('keydown',event=>{const target=event.target.closest('.history-point');if(target&&(event.key==='Enter'||event.key===' ')){event.preventDefault();openEntity(target.dataset.entity);}});
  window.addEventListener('resize',()=>{if(state.tab==='records')drawScatter();if(state.tab==='map')drawMap();if(state.tab==='changes')renderPairs();});
  $('pairs').onpointermove=event=>{if(!pairsPlot)return;const [x,y]=pointPosition(event,$('pairs'));const point=nearest(pairsPlot.points,x,y);const pair=point?.pair;pointTooltip('pairs-tip',point,x,y,$('pairs'),pair?`<br>${pair.before_year} → ${pair.after_year}<br>Height ${fmt(pair.height_before)} → ${fmt(pair.height_after)} m<br>Arms ${fmt(pair.arms_before)} → ${fmt(pair.arms_after)}<br>Growth ${fmt(pair.annual_growth_m)} m/year`:'');};
  $('pairs').onclick=event=>{if(!pairsPlot)return;const [x,y]=pointPosition(event,$('pairs'));const point=nearest(pairsPlot.points,x,y);if(point)openEntity(point.pair.after_id);};
  $('pairs').onpointerleave=()=>$('pairs-tip').hidden=true;
  let scatterStart=null,scatterDragging=false;
  $('scatter').onpointerdown=event=>{if(!scatterPlot)return;scatterStart=pointPosition(event,$('scatter'));scatterDragging=false;$('scatter').setPointerCapture(event.pointerId);};
  $('scatter').onpointermove=event=>{
    if(!scatterPlot)return;const [x,y]=pointPosition(event,$('scatter'));
    if(scatterStart&&Math.hypot(x-scatterStart[0],y-scatterStart[1])>7){scatterDragging=true;drawScatter();const ctx=$('scatter').getContext('2d');ctx.strokeStyle='#42745b';ctx.fillStyle='#42745b22';ctx.fillRect(scatterStart[0],scatterStart[1],x-scatterStart[0],y-scatterStart[1]);ctx.strokeRect(scatterStart[0],scatterStart[1],x-scatterStart[0],y-scatterStart[1]);$('scatter-tip').hidden=true;return;}
    pointTooltip('scatter-tip',nearest(scatterPlot.points,x,y),x,y,$('scatter'));
  };
  $('scatter').onpointerup=event=>{
    if(!scatterStart||!scatterPlot)return;const [x,y]=pointPosition(event,$('scatter'));
    if(scatterDragging&&Math.abs(x-scatterStart[0])>10&&Math.abs(y-scatterStart[1])>10){const p=scatterPlot,[xmin,xmax,ymin,ymax]=p.domain;const ix=px=>xmin+(Math.max(p.left,Math.min(p.right,px))-p.left)/(p.right-p.left)*(xmax-xmin);const iy=py=>ymin+(p.bottom-Math.max(p.top,Math.min(p.bottom,py)))/(p.bottom-p.top)*(ymax-ymin);scatterBounds=[ix(Math.min(x,scatterStart[0])),ix(Math.max(x,scatterStart[0])),iy(Math.max(y,scatterStart[1])),iy(Math.min(y,scatterStart[1]))];if(scatterBounds[0]===scatterBounds[1]||scatterBounds[2]===scatterBounds[3])scatterBounds=null;drawScatter();}
    else if(!scatterDragging){const point=nearest(scatterPlot.points,x,y);if(point)openEntity(point.row.observation_id);}
    scatterStart=null;scatterDragging=false;
  };
  $('scatter').onpointerleave=()=>$('scatter-tip').hidden=true;
  let mapStart=null,mapDragged=false;
  $('map').onpointerdown=event=>{if(!mapPlot)return;mapStart={position:pointPosition(event,$('map')),bounds:[...mapBounds]};mapDragged=false;$('map').setPointerCapture(event.pointerId);};
  $('map').onpointermove=event=>{
    if(!mapPlot)return;const [x,y]=pointPosition(event,$('map'));
    if(mapStart&&Math.hypot(x-mapStart.position[0],y-mapStart.position[1])>4){mapDragged=true;const dx=(x-mapStart.position[0])/mapPlot.sx,dy=(y-mapStart.position[1])/mapPlot.sy;mapBounds=[mapStart.bounds[0]-dx,mapStart.bounds[1]-dx,mapStart.bounds[2]+dy,mapStart.bounds[3]+dy];drawMap();$('map-tip').hidden=true;return;}
    const point=nearest(mapPlot.points,x,y);
    pointTooltip('map-tip',point,x,y,$('map'),point?`<br><strong>${mapHistoryText(point.row)}</strong>`:'');
  };
  $('map').onpointerup=event=>{
    if(mapPlot&&mapStart&&!mapDragged){const [x,y]=pointPosition(event,$('map'));const point=nearest(mapPlot.points,x,y);if(point){const row=point.row;const colocated=baseRecords.filter(item=>item.longitude===row.longitude&&item.latitude===row.latitude);$('colocated').innerHTML=`<h3>${fmt(colocated.length)} records at ${row.longitude.toFixed(6)}, ${row.latitude.toFixed(6)}</h3><p class="caption">These records share source coordinates; co-location alone does not establish identity. Showing up to 50; use frame/year filters to narrow the selection.</p>${colocated.slice(0,50).map(item=>`<button data-entity="${item.observation_id}">${esc(label(item.program_id))} · ${item.survey_year} · ${esc(item.source_individual_id||item.observation_id.slice(0,9))}</button>`).join(' ')}`;openEntity(row.observation_id);}}
    mapStart=null;mapDragged=false;
  };
  $('map').onpointerleave=()=>$('map-tip').hidden=true;
  $('map').addEventListener('wheel',event=>{event.preventDefault();zoomMap(event.deltaY>0?1.18:.85,pointPosition(event,$('map')));},{passive:false});
}
async function start() {
  try {
    const response=await fetch('explorer/data.json');if(!response.ok)throw new Error('Research index request failed.');data=await response.json();
    observations=unpack(data.observation_columns,data.observations);findings=unpack(data.finding_columns,data.findings).map((row,index)=>({...row,index}));
    for(const kind of ['plot','vegetation'])summaryRows[kind]=unpack(data.summary_columns[kind],data.summaries[kind]);
    obsIndex=new Map(observations.map(row=>[row.observation_id,row]));organismIndex=new Map();entityFindings=new Map();
    for(const row of observations)if(row.organism_id){if(!organismIndex.has(row.organism_id))organismIndex.set(row.organism_id,[]);organismIndex.get(row.organism_id).push(row);}
    for(const row of findings){if(!entityFindings.has(row.entity_identifier))entityFindings.set(row.entity_identifier,[]);entityFindings.get(row.entity_identifier).push(row);}
    indexHistoryCoverage();
    $('map-color').prepend(new Option('Survey observation count','history',true,true));
    const allFrames=[...observations,...summaryRows.plot,...summaryRows.vegetation];
    $('program').innerHTML='<option value="">All frames</option>'+[...new Set([...allFrames.map(r=>r.program_id),...data.files.map(r=>r.dataset)])].sort().map(p=>`<option value="${esc(p)}">${esc(label(p))}</option>`).join('');
    $('year').innerHTML='<option value="">All years</option>'+[...new Set(allFrames.map(r=>r.survey_year).filter(Boolean))].sort((a,b)=>a-b).map(y=>`<option>${y}</option>`).join('');
    $('rule').innerHTML='<option value="">Every rule</option>'+[...new Set(findings.map(r=>r.rule_id))].sort().map(rule=>`<option>${esc(rule)}</option>`).join('');
    $('pair-interval').innerHTML='<option value="">All intervals</option>'+[...new Set(data.pairs.map(pair=>`${pair.before_year}–${pair.after_year}`))].sort().map(interval=>`<option>${esc(interval)}</option>`).join('');
    $('representation').innerHTML='<option value="">All representations</option>'+[...new Set(summaryRows.plot.map(row=>row.representation))].sort().map(value=>`<option>${esc(value)}</option>`).join('');
    $('limitations').innerHTML=data.summary.limitations.map(item=>`<li>${esc(item)}</li>`).join('');
    $('aggregate-note').innerHTML='<p class="caption">Aggregate count/density representations and vegetation summaries are preserved separately from the organism observations above. They overlap other representations and are not added to record totals.</p><div class="scroll"><table><thead><tr><th>Frame</th><th>Aggregate representation</th><th>Rows</th></tr></thead><tbody>'+data.aggregate_counts.map(row=>`<tr><td>${esc(label(row.program_id))}</td><td>${esc(row.representation)}</td><td>${fmt(row.records)}</td></tr>`).join('')+'</tbody></table></div>';
    readHash();
    $('map-background').value=state.mapBackground;
    for(const [key,id] of [['program','program'],['year','year'],['rule','rule'],['severity','severity'],['mode','record-mode'],['pairMeasure','pair-measure'],['pairInterval','pair-interval'],['summaryKind','summary-kind'],['representation','representation']]) {
      if(![...$(id).options].some(option=>option.value===state[key]))state[key]=$(id).options[0].value;
    }
    attachEvents();$('load-status').hidden=true;$('application').hidden=false;render();
    if(state.entity)openEntity(state.entity,state.fi);
    // A small, read-only inspection hook supports browser QA and external integrations.
    window.saguarodataExplorer={get counts(){return {observations:observations.length,findings:findings.length,selectedObservations:baseRecords.length,selectedFindings:visibleFindings.length};}};
  }catch(error){$('load-status').classList.add('error');$('load-status').innerHTML=`${esc(error.message)} Open this report through your local HTTP server (for example http://127.0.0.1:8000/data_quality_report.html), or use <a href="data_quality_report_static.html">the static report</a>.`;}
}
start();
