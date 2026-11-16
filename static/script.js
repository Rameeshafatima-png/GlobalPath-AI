const form=document.querySelector("#form"),btn=document.querySelector("#submit"),err=document.querySelector("#error"),results=document.querySelector("#results");
const esc=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const ul=a=>Array.isArray(a)&&a.length?`<ul>${a.map(x=>`<li>${esc(x)}</li>`).join("")}</ul>`:"<p class='muted'>No details returned.</p>";
const card=(t,b)=>`<article class="panel"><h3>${t}</h3>${b}</article>`;
function render(d){
document.querySelector("#summary").innerHTML=`<h3>Profile analysis</h3><p>${esc(d.profile_summary)}</p><p>${esc(d.suitability_analysis)}</p>`;
const uni=(d.universities||[]).map((u,i)=>`<div class="uni"><b>${String(i+1).padStart(2,"0")}</b><div><h4>${esc(u.name)}</h4><small>${esc(u.location)}</small><p>${esc(u.program)}</p><p><strong>Tuition estimate:</strong> ${esc(u.tuition_estimate)}</p><p>${esc(u.fit_reason)}</p><p>${esc((u.scholarship_options||[]).join(", "))}</p>${u.official_url?`<a href="${esc(u.official_url)}" target="_blank" rel="noopener">Official website ↗</a>`:""}</div></div>`).join("")||"<p class='muted'>No university options returned.</p>";
const costs=(d.cost_breakdown||[]).map(c=>`<div class="cost"><b>${esc(c.category)}</b><strong>${esc(c.estimate)}</strong><small>${esc(c.notes)}</small></div>`).join("");
const road=(d.application_roadmap||[]).map(x=>`<li>${esc(x)}</li>`).join("");
document.querySelector("#cards").innerHTML=[
card("University shortlist",uni),card("Degree recommendations",ul(d.degree_recommendations)),
card("Scholarship opportunities",ul(d.scholarships)),card("Profile-building activities",ul(d.activities)),
card("Estimated cost breakdown",costs),card("Application roadmap",`<ol>${road}</ol>`),card("Important notes",ul(d.important_notes))
].join("");
const src=(d.sources||[]).filter(Boolean);
document.querySelector("#sources").innerHTML=`<h3>Research sources</h3>${src.length?src.map(s=>`<p><a href="${esc(s)}" target="_blank" rel="noopener">${esc(s)} ↗</a></p>`).join(""):"<p class='muted'>No live source links returned. Verify details on official websites.</p>"}<p class="disclaimer">${esc(d.disclaimer)}</p>`;
results.classList.remove("hidden");results.scrollIntoView({behavior:"smooth"});
}
form.addEventListener("submit",async e=>{e.preventDefault();err.classList.add("hidden");results.classList.add("hidden");btn.disabled=true;btn.textContent="Researching your options...";
const payload=Object.fromEntries(new FormData(form).entries());payload.budget=Number(payload.budget);
try{const r=await fetch("/api/study-plan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});const d=await r.json();if(!r.ok)throw Error(d.detail||"Request failed");render(d);}
catch(ex){err.textContent=ex.message;err.classList.remove("hidden");}finally{btn.disabled=false;btn.textContent="Generate my study plan →";}});
