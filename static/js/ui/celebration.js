import { markCelebrated } from '../services/store.js';
import { showToast, showBigToast } from './ui.js';

function rgba(hex, alpha=0.8){ const m=/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex); if(!m) return hex; const r=parseInt(m[1],16), g=parseInt(m[2],16), b=parseInt(m[3],16); return `rgba(${r}, ${g}, ${b}, ${alpha})`; }

export function startConfetti(){ const prefersReduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches; const emojis=['🎉','🎊','✨','🥳','🌟','💥','💫','🎈']; const colors=['#ff4d4f','#ffd666','#36cfc9','#40a9ff','#73d13d','#9254de','#f759ab','#fa8c16']; const emojiCount=prefersReduce?0:90; const pieceCount=prefersReduce?0:120; for(let i=0;i<emojiCount;i++){ const el=document.createElement('span'); el.className='confetti'; el.textContent=emojis[Math.floor(Math.random()*emojis.length)]; el.style.left=(Math.random()*100)+'vw'; el.style.fontSize=(14+Math.random()*20)+'px'; el.style.animationDuration=(3.5+Math.random()*3)+'s'; document.body.appendChild(el); setTimeout(()=>el.remove(),7000);} for(let i=0;i<pieceCount;i++){ const el=document.createElement('span'); el.className='confetti confetti-piece'; el.style.left=(Math.random()*100)+'vw'; el.style.backgroundColor=rgba(colors[Math.floor(Math.random()*colors.length)],0.78); el.style.animationDuration=(3.2+Math.random()*3)+'s'; el.style.borderRadius=Math.random()<0.35?'50%':'2px'; document.body.appendChild(el); setTimeout(()=>el.remove(),7000);} }

// Celebrate skill achievement (goal reached or full mastery)
// markCelebrated persists to localStorage so we don't re-celebrate on refresh
// unmarkCelebrated is called separately when a goal is cleared (see clearGoal in standalone.js)
export function celebrateSkill(learnerId, skillName, skillId, type='goal'){ markCelebrated(learnerId, skillId, type); const msg=type==='full'?`Amazing! You've fully mastered ${skillName}!`:`Well done! You reached your goal for ${skillName}!`; showToast(msg); showBigToast(msg); startConfetti(); }

export function renderCourseComplete(){ const board=document.getElementById('board'); if(!board) return; board.innerHTML=`<div class="complete-wrap" style="grid-column:1 / -1"><div><div class="complete-title">Course complete! 🏆🎉</div><div class="complete-sub mt-2">You've mastered everything. Fantastic work! 🎊</div><a href="certificate.html" class="btn btn-lg mt-4" style="background:linear-gradient(135deg,#b8972e,#d4af37);color:#fff;font-weight:600;padding:12px 32px;border-radius:8px;text-decoration:none;display:inline-block">Claim Your Certificate</a></div></div>`; startConfetti(); }
