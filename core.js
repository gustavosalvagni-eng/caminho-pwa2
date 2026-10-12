/* Caminho 2.0 — utilitários sem dependências, compartilhados com os testes. */
(function(root){
'use strict';
const normal=s=>String(s).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function parseJournal(raw){
 const data=JSON.parse(raw),rows=Array.isArray(data)?data:data?.schema==='caminho.diary'&&data.version===2?data.entries:null;
 if(!Array.isArray(rows)||rows.length>10000)throw new Error('Formato de diário não reconhecido. Nenhum registro foi alterado.');
 for(const row of rows){if(!row||typeof row!=='object'||Array.isArray(row))throw new Error('Registro inválido.');for(const k of ['date','reading','motion','purpose'])if(typeof row[k]!=='string'||row[k].length>20000)throw new Error('Campos do diário inválidos.');if(row.id!==undefined&&(typeof row.id!=='string'||row.id.length>100))throw new Error('Identificador inválido.');}
 return rows;
}
const signature=e=>JSON.stringify([e.date,e.reading,e.motion,e.purpose]);
function mergeJournal(oldRows,newRows){const seen=new Set(oldRows.map(signature));const result=oldRows.slice();for(const e of newRows)if(!seen.has(signature(e))){result.push(e);seen.add(signature(e));}return result;}
function speechChunks(text){const words=String(text).trim().split(/\s+/);const out=[];let part='';for(let word of words){if(word.length>220){if(part){out.push(part);part='';}while(word.length>220){out.push(word.slice(0,220));word=word.slice(220);}}if(part.length+word.length+1>220){out.push(part);part=word;}else part+=(part?' ':'')+word;}if(part)out.push(part);return out;}
const mysteryForDay=day=>['Gloriosos','Gozosos','Dolorosos','Gloriosos','Luminosos','Dolorosos','Gozosos'][day];
const X={normal,escape,parseJournal,mergeJournal,speechChunks,mysteryForDay};root.CaminhoCore=X;if(typeof module!=='undefined')module.exports=X;
})(globalThis);
