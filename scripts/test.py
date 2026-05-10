import pandas as pd
import json

# -----------------------------
# INPUT / OUTPUT
# -----------------------------
csv_file = "../data/smmh.csv"
out_html = "../html-files/ster.html"

df = pd.read_csv(csv_file)

# -----------------------------
# COLUMNS
# -----------------------------
platform_col = "7. What social media platforms do you commonly use?"

question_cols = {
    "Q9": "9. How often do you find yourself using Social media without a specific purpose?",
    "Q10": "10. How often do you get distracted by Social media when you are busy doing something?",
    "Q11": "11. Do you feel restless if you haven't used Social media in a while?",
    "Q12": "12. On a scale of 1 to 5, how easily distracted are you?",
    "Q13": "13. On a scale of 1 to 5, how much are you bothered by worries?",
    "Q14": "14. Do you find it difficult to concentrate on things?",
    "Q15": "15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?",
    "Q16": "16. Following the previous question, how do you feel about these comparisons, generally speaking?",
    "Q17": "17. How often do you look to seek validation from features of social media?",
    "Q18": "18. How often do you feel depressed or down?",
    "Q19": "19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?",
    "Q20": "20. On a scale of 1 to 5, how often do you face issues regarding sleep?"
}

question_labels = {
    "Q9": "Purposeless use",
    "Q10": "Distracted while busy",
    "Q11": "Restless offline",
    "Q12": "Easily distracted",
    "Q13": "Bothered by worries",
    "Q14": "Concentration issues",
    "Q15": "Social comparison",
    "Q16": "Feeling after comparison",
    "Q17": "Validation seeking",
    "Q18": "Feeling down",
    "Q19": "Interest fluctuation",
    "Q20": "Sleep issues"
}

platforms = [
    "Instagram", "Facebook", "Twitter", "YouTube", "Discord",
    "Pinterest", "TikTok", "Snapchat", "Reddit", "LinkedIn"
]

# -----------------------------
# SUMMARISE DATA
# -----------------------------
rows = []

for platform in platforms:
    sub = df[
        df[platform_col]
        .fillna("")
        .str.contains(platform, case=False, regex=False)
    ]

    if sub.empty:
        continue

    scores = {}
    for q, col in question_cols.items():
        scores[q] = round(pd.to_numeric(sub[col], errors="coerce").mean(), 2)

    rows.append({
        "platform": platform,
        "n": int(len(sub)),
        "avgAge": round(pd.to_numeric(sub["1. What is your age?"], errors="coerce").mean(), 1),
        "occupation": sub["4. Occupation Status"].value_counts().to_dict(),
        "scores": scores
    })

story_data = {
    "platforms": rows,
    "questions": [
        {
            "id": q,
            "short": question_labels[q],
            "full": question_cols[q]
        }
        for q in question_cols
    ]
}

DATA_JSON = json.dumps(story_data, indent=2)

# -----------------------------
# HTML TEMPLATE
# -----------------------------
html = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Was Grandma Right?</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>

<style>
:root {
  --cream:#F5F0E8;
  --dark:#1A1209;
  --warm:#C8A96E;
  --accent:#E8472A;
  --muted:#6B5E4A;
  --card:#FFFDF7;
  --border:rgba(200,169,110,0.28);
}

* {
  box-sizing:border-box;
  margin:0;
  padding:0;
}

body {
  background:var(--cream);
  color:var(--dark);
  font-family:'DM Sans',sans-serif;
  font-weight:300;
  line-height:1.7;
  overflow-x:hidden;
}

.hero {
  min-height:80vh;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  text-align:center;
  padding:4rem 2rem;
  position:relative;
}

.hero::before {
  content:'';
  position:absolute;
  inset:0;
  background:
    repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(200,169,110,0.11) 39px,rgba(200,169,110,0.11) 40px),
    repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(200,169,110,0.11) 39px,rgba(200,169,110,0.11) 40px);
  pointer-events:none;
}

.eyebrow {
  font-family:'DM Mono',monospace;
  font-size:11px;
  letter-spacing:.22em;
  text-transform:uppercase;
  color:var(--muted);
  margin-bottom:2rem;
  position:relative;
}

h1 {
  font-family:'Playfair Display',serif;
  font-size:clamp(3rem,8vw,7rem);
  font-weight:900;
  line-height:1;
  max-width:950px;
  position:relative;
}

h1 em {
  color:var(--accent);
}

.hero-sub {
  max-width:560px;
  color:var(--muted);
  margin-top:1.75rem;
  position:relative;
}

section {
  max-width:1100px;
  margin:0 auto;
  padding:5rem 2rem;
}

.sec-label {
  font-family:'DM Mono',monospace;
  font-size:10px;
  letter-spacing:.25em;
  text-transform:uppercase;
  color:var(--warm);
  margin-bottom:.9rem;
}

h2 {
  font-family:'Playfair Display',serif;
  font-size:clamp(2rem,4vw,3rem);
  line-height:1.15;
  margin-bottom:.9rem;
}

.lead {
  max-width:680px;
  color:var(--muted);
  margin-bottom:2rem;
}

.card {
  background:var(--card);
  border:1px solid var(--border);
  border-radius:18px;
  padding:2rem;
  margin-bottom:1.5rem;
}

.controls {
  display:flex;
  flex-wrap:wrap;
  gap:.6rem;
  margin-bottom:1.8rem;
}

.check {
  font-family:'DM Mono',monospace;
  font-size:10px;
  letter-spacing:.08em;
  text-transform:uppercase;
  padding:.45rem .75rem;
  border:1px solid var(--border);
  border-radius:999px;
  background:rgba(255,253,247,.7);
  cursor:pointer;
}

.check input {
  margin-right:.35rem;
}

.chart-wrap {
  position:relative;
  height:520px;
}

.word-map-card {
  background:var(--dark);
  color:var(--cream);
  border-radius:24px;
  padding:2.4rem;
  border:1px solid rgba(200,169,110,.25);
}

.word-map-top {
  display:flex;
  justify-content:space-between;
  gap:1rem;
  flex-wrap:wrap;
  margin-bottom:2rem;
}

.word-question {
  max-width:620px;
}

.word-question-label {
  font-family:'DM Mono',monospace;
  font-size:10px;
  letter-spacing:.18em;
  text-transform:uppercase;
  color:var(--warm);
  margin-bottom:.4rem;
}

.word-question-title {
  font-family:'Playfair Display',serif;
  font-size:2rem;
  line-height:1.1;
}

.word-question-full {
  color:rgba(245,240,232,.6);
  font-size:.9rem;
  margin-top:.6rem;
}

.word-buttons {
  display:flex;
  flex-wrap:wrap;
  gap:.45rem;
  max-width:430px;
}

.word-btn {
  border:1px solid rgba(200,169,110,.25);
  background:rgba(245,240,232,.04);
  color:rgba(245,240,232,.78);
  font-family:'DM Mono',monospace;
  font-size:10px;
  letter-spacing:.08em;
  border-radius:999px;
  padding:.42rem .7rem;
  cursor:pointer;
  transition:all .2s;
}

.word-btn:hover,
.word-btn.active {
  background:var(--warm);
  color:var(--dark);
}

.word-map {
  min-height:360px;
  display:flex;
  flex-wrap:wrap;
  justify-content:center;
  align-items:center;
  gap:1.1rem 1.6rem;
  padding:2rem;
  border-radius:18px;
  background:
    radial-gradient(circle at 20% 20%, rgba(232,71,42,.12), transparent 28%),
    radial-gradient(circle at 80% 50%, rgba(200,169,110,.12), transparent 30%),
    rgba(245,240,232,.035);
  border:1px solid rgba(200,169,110,.18);
}

.word {
  font-family:'Playfair Display',serif;
  font-weight:900;
  line-height:1;
  display:inline-flex;
  align-items:center;
  gap:.35rem;
  opacity:0;
  animation:popIn .65s cubic-bezier(.2,.9,.2,1) forwards;
  transition:transform .25s, filter .25s;
  text-shadow:0 8px 28px rgba(0,0,0,.18);
}

.word:hover {
  filter:brightness(1.2);
  transform:scale(1.08);
}

.word-score {
  font-family:'DM Mono',monospace;
  font-size:.65rem;
  font-weight:400;
  color:rgba(245,240,232,.55);
}

@keyframes popIn {
  from {
    transform:scale(.4) translateY(18px);
    opacity:0;
  }
  to {
    transform:scale(1) translateY(0);
    opacity:1;
  }
}

.word-legend {
  display:flex;
  gap:1rem;
  flex-wrap:wrap;
  margin-top:1rem;
  color:rgba(245,240,232,.55);
  font-family:'DM Mono',monospace;
  font-size:10px;
}

.word-legend strong {
  color:var(--warm);
  font-weight:500;
}

.story-box {
  background:var(--dark);
  color:var(--cream);
  border-radius:22px;
  padding:3rem;
  margin-top:2rem;
}

.story-box h3 {
  font-family:'Playfair Display',serif;
  font-size:2rem;
  margin-bottom:1rem;
}

.story-box p {
  color:rgba(245,240,232,.72);
  max-width:760px;
  margin-bottom:1rem;
}

.verdict {
  display:inline-block;
  font-family:'DM Mono',monospace;
  font-size:9px;
  letter-spacing:.12em;
  text-transform:uppercase;
  border-radius:999px;
  padding:.2rem .55rem;
  margin-left:.4rem;
}

.v-supported {
  background:rgba(232,71,42,.18);
  color:#FFD9D2;
}

.v-partly {
  background:rgba(200,169,110,.2);
  color:#F5DDA4;
}

.v-weak {
  background:rgba(245,240,232,.12);
  color:rgba(245,240,232,.7);
}

@media(max-width:700px) {
  .chart-wrap {
    height:480px;
  }

  .word-map-card {
    padding:1.4rem;
  }

  .word-map {
    min-height:420px;
    padding:1.4rem;
  }
}
</style>
</head>

<body>

<div class="hero">
  <p class="eyebrow">Social media platforms · questions 9–20</p>
  <h1>Was <em>grandma</em> right?</h1>
  <p class="hero-sub">
    Choose one or more platforms and compare how users score across purposeless use,
    distraction, worries, validation seeking, mood, and sleep.
  </p>
</div>

<section>
  <p class="sec-label">01 — Platform comparison</p>
  <h2>Which platforms are linked to which feelings?</h2>
  <p class="lead">
    Select apps below. Each line shows the average score from 1 to 5 for users of that platform.
    Higher means the behaviour or feeling was reported more often.
  </p>

  <div class="card">
    <div class="controls" id="platformControls"></div>
    <div class="chart-wrap">
      <canvas id="scoreChart"></canvas>
    </div>
  </div>
</section>

<section>
  <p class="sec-label">02 — Strongest platform signal</p>
  <h2>A word map of platform associations.</h2>
  <p class="lead">
    Pick a question. The platform names grow larger when their average score is higher.
  </p>

  <div class="word-map-card">
    <div class="word-map-top">
      <div class="word-question">
        <p class="word-question-label" id="wordQuestionID">Q17</p>
        <h3 class="word-question-title" id="wordQuestionTitle">Validation seeking</h3>
        <p class="word-question-full" id="wordQuestionFull"></p>
      </div>

      <div class="word-buttons" id="wordButtons"></div>
    </div>

    <div class="word-map" id="wordMap"></div>

    <div class="word-legend">
      <span><strong>Bigger</strong> = higher average score</span>
      <span><strong>Score range</strong> = 1 to 5</span>
      <span><strong>Ties</strong> appear at the same size</span>
    </div>
  </div>
</section>

<section>
  <p class="sec-label">03 — So are they true?</p>
  <h2>Testing the stereotypes.</h2>
  <p class="lead">
    We all have assumptions about different platforms. This section checks whether the data actually supports them.
  </p>

  <div class="card">
    <div class="chart-wrap" style="height:420px;">
      <canvas id="stereoChart"></canvas>
    </div>
  </div>

  <div class="story-box">
    <h3>What the data says</h3>
    <div id="stereotypeText"></div>
  </div>
</section>

<script>
const D = __DATA_JSON__;

const QUESTION_COLORS = {
  Q9:  "#E8472A",
  Q10: "#C8A96E",
  Q11: "#534AB7",
  Q12: "#185FA5",
  Q13: "#D4537E",
  Q14: "#3B6D11",
  Q15: "#BA7517",
  Q16: "#888780",
  Q17: "#0F6E56",
  Q18: "#A64253",
  Q19: "#6F4E37",
  Q20: "#2F4858"
};

const PLATFORM_COLORS = [
  "#E8472A","#C8A96E","#534AB7","#185FA5","#D4537E",
  "#3B6D11","#BA7517","#888780","#0F6E56","#A64253"
];

Chart.defaults.font.family = "'DM Mono', monospace";
Chart.defaults.color = "#6B5E4A";

const qIDs = D.questions.map(q => q.id);
const qLabels = D.questions.map(q => q.short);

/* -----------------------------
   SECTION 01: LINE CHART
----------------------------- */
const platformControls = document.getElementById("platformControls");

D.platforms.forEach((p) => {
  const checked = ["Instagram", "TikTok", "YouTube"].includes(p.platform) ? "checked" : "";

  platformControls.innerHTML += `
    <label class="check">
      <input type="checkbox" value="${p.platform}" ${checked} onchange="updateChart()">
      ${p.platform}
    </label>
  `;
});

const scoreChart = new Chart(document.getElementById("scoreChart"), {
  type: "line",
  data: {
    labels: qLabels,
    datasets: []
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: "nearest",
      intersect: false
    },
    plugins: {
      legend: {
        position: "bottom"
      },
      tooltip: {
        callbacks: {
          title: items => {
            const idx = items[0].dataIndex;
            return D.questions[idx].id + " — " + D.questions[idx].short;
          },
          afterTitle: items => {
            const idx = items[0].dataIndex;
            return D.questions[idx].full;
          },
          label: item => `${item.dataset.label}: ${item.parsed.y.toFixed(2)} / 5`
        }
      }
    },
    scales: {
      y: {
        min: 1,
        max: 5,
        ticks: {
          callback: value => value + "/5"
        },
        grid: {
          color: "rgba(200,169,110,0.15)"
        }
      },
      x: {
        ticks: {
          maxRotation: 55,
          minRotation: 35,
          color: ctx => QUESTION_COLORS[qIDs[ctx.index]]
        },
        grid: {
          display: false
        }
      }
    }
  }
});

function updateChart() {
  const selected = [...document.querySelectorAll("#platformControls input:checked")]
    .map(x => x.value);

  scoreChart.data.datasets = D.platforms
    .filter(p => selected.includes(p.platform))
    .map((p) => {
      const col = PLATFORM_COLORS[
        D.platforms.findIndex(x => x.platform === p.platform) % PLATFORM_COLORS.length
      ];

      return {
        label: `${p.platform} (n=${p.n})`,
        data: qIDs.map(q => p.scores[q]),
        borderColor: col,
        backgroundColor: col + "33",
        pointBackgroundColor: qIDs.map(q => QUESTION_COLORS[q]),
        pointBorderColor: "#1A1209",
        pointRadius: 5,
        pointHoverRadius: 8,
        tension: 0.25,
        borderWidth: 2
      };
    });

  scoreChart.update();
}

/* -----------------------------
   SECTION 02: WORD MAP
----------------------------- */
const wordButtons = document.getElementById("wordButtons");

D.questions.forEach(q => {
  const active = q.id === "Q17" ? "active" : "";

  wordButtons.innerHTML += `
    <button class="word-btn ${active}" onclick="renderWordMap('${q.id}', this)">
      ${q.id}
    </button>
  `;
});

function renderWordMap(qID, btn=null) {
  if (btn) {
    document.querySelectorAll(".word-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
  }

  const q = D.questions.find(x => x.id === qID);

  document.getElementById("wordQuestionID").textContent = q.id;
  document.getElementById("wordQuestionTitle").textContent = q.short;
  document.getElementById("wordQuestionFull").textContent = q.full;

  const values = D.platforms.map(p => p.scores[qID]);
  const minScore = Math.min(...values);
  const maxScore = Math.max(...values);

  const sorted = [...D.platforms].sort((a, b) => b.scores[qID] - a.scores[qID]);

  const wordMap = document.getElementById("wordMap");
  wordMap.innerHTML = "";

  sorted.forEach((p, i) => {
    const score = p.scores[qID];

    const scaled = maxScore === minScore
      ? 0.7
      : (score - minScore) / (maxScore - minScore);

    const fontSize = 1.1 + scaled * 3.4;
    const opacity = 0.45 + scaled * 0.55;
    const color = score === maxScore ? QUESTION_COLORS[qID] : `rgba(245,240,232,${opacity})`;

    const span = document.createElement("span");
    span.className = "word";
    span.style.fontSize = fontSize + "rem";
    span.style.color = color;
    span.style.animationDelay = (i * 70) + "ms";
    span.title = p.platform + ": " + score.toFixed(2) + " / 5";

    span.innerHTML = `
      ${p.platform}
      <span class="word-score">${score.toFixed(2)}</span>
    `;

    wordMap.appendChild(span);
  });
}

/* -----------------------------
   SECTION 03: STEREOTYPE CHECK
----------------------------- */
const stereotypes = [
  {
    platform: "YouTube",
    question: "Q20",
    claim: "YouTube users have trouble sleeping"
  },
  {
    platform: "Instagram",
    question: "Q15",
    claim: "Instagram users compare themselves to others"
  },
  {
    platform: "Facebook",
    question: "Q9",
    claim: "Facebook users scroll without a clear purpose"
  },
  {
    platform: "Twitter",
    question: "Q18",
    claim: "Twitter users feel depressed or down"
  },
  {
    platform: "TikTok",
    question: "Q14",
    claim: "TikTok users have concentration issues"
  },
  {
    platform: "Snapchat",
    question: "Q17",
    claim: "Snapchat users seek validation"
  },
  {
    platform: "Discord",
    question: "Q11",
    claim: "Discord users feel restless offline"
  },
  {
    platform: "Pinterest",
    question: "Q16",
    claim: "Pinterest users feel affected by comparisons"
  },
  {
    platform: "Reddit",
    question: "Q13",
    claim: "Reddit users are bothered by worries"
  },
  {
    platform: "LinkedIn",
    question: "Q15",
    claim: "LinkedIn users compare themselves to successful people"
  }
];

function getPlatform(platformName) {
  return D.platforms.find(p => p.platform === platformName);
}

function getQuestion(qID) {
  return D.questions.find(q => q.id === qID);
}

function rankPlatform(platformName, qID) {
  const sorted = [...D.platforms].sort((a, b) => b.scores[qID] - a.scores[qID]);
  return sorted.findIndex(p => p.platform === platformName) + 1;
}

function makeStereotypeSection() {
  const rows = stereotypes
    .filter(s => getPlatform(s.platform))
    .map(s => {
      const p = getPlatform(s.platform);
      const q = getQuestion(s.question);
      const score = p.scores[s.question];
      const rank = rankPlatform(s.platform, s.question);

      let verdict = "Weak";
      if (rank === 1) verdict = "Supported";
      else if (rank <= 3) verdict = "Partly supported";

      return {
        ...s,
        score,
        rank,
        verdict,
        questionLabel: q.short
      };
    });

  new Chart(document.getElementById("stereoChart"), {
    type: "bar",
    data: {
      labels: rows.map(r => r.platform),
      datasets: [{
        label: "Score for stereotype-related question",
        data: rows.map(r => r.score),
        backgroundColor: rows.map(r => {
          if (r.verdict === "Supported") return "#E8472A";
          if (r.verdict === "Partly supported") return "#C8A96E";
          return "#888780";
        }),
        borderColor: "#1A1209",
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          callbacks: {
            title: items => rows[items[0].dataIndex].claim,
            label: item => {
              const r = rows[item.dataIndex];
              return [
                `Score: ${r.score.toFixed(2)} / 5`,
                `Question: ${r.questionLabel}`,
                `Rank: #${r.rank} among platforms`,
                `Verdict: ${r.verdict}`
              ];
            }
          }
        }
      },
      scales: {
        y: {
          min: 1,
          max: 5,
          ticks: {
            callback: value => value + "/5"
          },
          grid: {
            color: "rgba(200,169,110,0.15)"
          }
        },
        x: {
          grid: {
            display: false
          },
          ticks: {
            font: {
              size: 10
            }
          }
        }
      }
    }
  });

  document.getElementById("stereotypeText").innerHTML = rows.map(r => {
    const cls =
      r.verdict === "Supported"
        ? "v-supported"
        : r.verdict === "Partly supported"
          ? "v-partly"
          : "v-weak";

    return `
      <p>
        <strong>${r.platform}</strong> — ${r.claim}
        <span class="verdict ${cls}">${r.verdict}</span><br>
        Score: <strong>${r.score.toFixed(2)} / 5</strong>.
        Rank: <strong>#${r.rank}</strong> for ${r.questionLabel}.
      </p>
    `;
  }).join("");
}

updateChart();
renderWordMap("Q17");
makeStereotypeSection();
</script>

</body>
</html>
"""

html = html.replace("__DATA_JSON__", DATA_JSON)

with open(out_html, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Saved clean HTML to: {out_html}")