from pathlib import Path
p=Path("_site/index.html")
html=p.read_text(encoding="utf-8")
html=html.replace("Phase 1 — v13","Phase 1 — v14")
review_handler="""   btn.onclick=()=>{
    let score=0,answered=0;
    const responses=[];
    assessments[id].forEach((q,i)=>{let x=form.querySelector(`input[name="${id}${i}"]:checked`);if(x){answered++;const chosen=+x.value;const correct=chosen===q.a;if(correct)score++;responses.push({i,chosen,correct});}});
    if(answered<assessments[id].length){alert("Please answer every question.");return;}
    let pct=Math.round(score/assessments[id].length*100);
    let status=pct>=90?"Mastered":pct>=75?"Developing":"Needs Practice";
    let r=document.createElement("div");r.className="result";let advice=pct>=90?"Strong work. Keep this skill active with spaced revision.":pct>=75?"You are developing this skill. Review the questions you missed, then try again later.":"Let's strengthen the foundation. Review the explanation, practise slowly, then reassess.";
    r.innerHTML=`<strong>Score: ${score}/${assessments[id].length} (${pct}%)</strong><br>Status: ${status}<br><span class="small">${advice}</span><hr><h4>📘 Review your answers</h4><div class="answer-review">${responses.map(x=>{const q=assessments[id][x.i];const chosen=q.o[x.chosen];const correct=q.o[q.a];const why=questionWhy(id,q);return `<div class="review-item ${x.correct?'review-correct':'review-learning'}"><strong>${x.i+1}. ${q.q}</strong><div class="small">Your answer: <strong>${chosen}</strong> ${x.correct?'✓':'✗'}</div>${x.correct?`<div class="review-explain"><strong>Why:</strong> ${why}</div>`:`<div class="review-explain"><strong>Correct answer:</strong> ${correct}<br><strong>Why:</strong> ${why}<br><strong>Try this:</strong> ${nextStep(id)}</div>`}</div>`}).join('')}</div>`;
    box.appendChild(r);localStorage.setItem("score_"+id,pct);
    const history=getHistory(id);
    history.push({ts:Date.now(),score,pct,total:assessments[id].length,answers:responses});
    saveHistory(id,history);
    localStorage.setItem("attempt_"+id,Date.now());
    updateStats(); renderHistory();
    btn.disabled=true;btn.textContent="Assessment reviewed";
   };
"""
import re
m=re.search(r'btn\.onclick=\(\)=>\{.*?\n\s*\};\n',html,re.S)
if not m: raise SystemExit("assessment handler target not found")
html=html[:m.start()]+review_handler+html[m.end():]
helpers="""const whyByTopic={
 M01:"Look at the place or number pattern carefully before choosing. In number sense, each digit has a value based on its position.",
 M02:"Calculate using place value, then estimate or check whether the result is reasonable.",
 M03:"Multiplication represents equal groups. For example, 6 × 4 means 6 groups of 4, or 4 + 4 + 4 + 4 + 4 + 4.",
 M04:"Division means sharing equally or finding how many equal groups fit. Use the matching multiplication fact to check.",
 M05:"First identify what is happening in the story. Then choose the operation that represents that situation before calculating.",
 M06:"A fraction describes equal parts of a whole. The numerator tells how many parts we have; the denominator tells how many equal parts make the whole.",
 M07:"Convert between familiar units using known relationships, and check that the unit matches what is being measured.",
 M08:"Use the defining properties of each shape rather than judging only by how it looks.",
 M09:"Use mental strategies such as doubles, halves, friendly numbers and compensation to calculate efficiently.",
 M10:"Use the number of units and their value carefully. For time, count forward in minutes and convert between minutes and hours when needed.",
 M11:"A factor divides a number exactly; a multiple is made by multiplying. Prime numbers have exactly two factors.",
 M12:"Read decimal place value from left to right. Tenths and hundredths are different sizes even when the digits look similar.",
 M13:"A ratio compares quantities. Equivalent ratios are made by multiplying or dividing both parts by the same number.",
 M14:"Percent means 'out of 100'. Connect common percentages to fractions and simple mental calculations.",
 M15:"Average is found by adding the values and dividing by how many values there are.",
 M16:"Profit is selling price minus cost price when the selling price is higher; loss is cost price minus selling price when it is lower.",
 M17:"Simple interest depends on principal, rate and time. Calculate the interest first, then add it to the principal to get amount.",
 M18:"Perimeter measures the distance around a shape; area measures the space inside it. Keep the units straight.",
 M19:"Volume measures the space occupied by a solid. For a cuboid, multiply length × breadth × height.",
 M20:"Speed connects distance and time. Use the relationship speed = distance ÷ time and check the units.",
 R01:"Look for the simplest repeating rule first: addition, subtraction, multiplication, division or a consistent pattern."
};
function questionWhy(id,q){
 const base=whyByTopic[id]||"Use the information in the question carefully and check your answer against the rule being tested.";
 const correct=q.o[q.a];
 return `${base} The correct choice here is <strong>${correct}</strong>.`;
}
function nextStep(id){
 const names={M03:"Practise the multiplication facts aloud and use equal-group pictures before increasing speed.",M01:"Practise place value and comparing numbers using short number sets.",M02:"Do a few untimed calculations, then add estimation checks.",M04:"Use multiplication facts to build division recall.",M05:"Underline the important facts in each word problem and name the operation before solving.",R01:"Try three new number patterns and say the rule aloud before choosing the next number."};
 return names[id]||"Review the lesson example, practise a few similar questions, and try this assessment again later.";
}

"""
if "const whyByTopic=" not in html:
    marker='let active="Mathematics";'
    if marker not in html: raise SystemExit("helper insertion point not found")
    html=html.replace(marker,helpers+'const MISSION_NDA_PROGRESS_SCHEMA="missionNDA_progress_v1";\\n'+marker,1)
css=".answer-review{margin-top:10px}.review-item{padding:10px 0;border-top:1px solid #e5e7eb}.review-correct{border-left:4px solid #6b8e6b;padding-left:10px}.review-learning{border-left:4px solid #c28a4a;padding-left:10px}.review-explain{margin-top:7px;font-size:.93rem;line-height:1.5}.result hr{border:0;border-top:1px solid #ddd;margin:14px 0}.result button{margin-top:8px}"
if ".answer-review{" not in html: html=html.replace("</style>",css+"</style>",1)
p.write_text(html,encoding="utf-8")
