# app.py (komplett)
import os

from flask import Flask

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <title>Ja / Nein</title>

  <style>
  body { 
    font-family: 'Georgia', serif;
    text-align: center; 
    margin: 0;
    padding-top: 80px;
    min-height: 100vh;
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  }

  h1 {
    margin-bottom: 60px;
    margin-left: 80px;
  }

  button {
    position: absolute;
    padding: 15px 30px;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
    border: none;
    border-radius: 50px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    transition: transform 0.25s ease, left 0.25s ease, top 0.25s ease;
    color: white;
    user-select: none;
    white-space: nowrap;
  }

  #yes {
    left: 40%;
    top: 520px;
    background: linear-gradient(45deg, #00b894, #55efc4);
    z-index: 1;
  }

  #no {
    left: 60%;
    top: 520px;
    background: linear-gradient(45deg, #ff4757, #ff6b9d);
    z-index: 2;
  }

  #cat-img {
    position: relative;
    width: 200px;
    margin: 20px auto 40px;  /* margins → margin */
    display: block;
    z-index: 10;  /* Über Buttons */
  }

  #success-img {
    display: none;
    width: 400px;
    margin: 40px auto;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  }
  </style>
</head>

<body>

  <h1 id="title">Haben wir am 14.02.2026 ein Date? 🤍</h1>

  <img id="cat-img" src="/static/cat.gif" alt="happy">

  <button id="yes">Ja</button>
  <button id="no">Nein</button>

  <img id="success-img" src="/static/verstappen.png" alt="Erfolg!">

  <audio id="success-sound" preload="auto">
    <source src="/static/romantic.mp3" type="audio/mpeg">
  </audio>

  <script>
    const yesBtn = document.getElementById("yes");
    const noBtn  = document.getElementById("no");
    const title  = document.getElementById("title");
    const img    = document.getElementById("success-img");
    const sound  = document.getElementById("success-sound");
    const gif    = document.getElementById("cat-img");

    let scale = 1;
    const TOP_MARGIN = 20;

    function growYes() {
    
      scale += 0.15;
      yesBtn.style.transform = `scale(${scale})`;

      keepYesBelowTitle();
      keepNoAway();
    }

    function keepYesBelowTitle() {
      const titleRect = title.getBoundingClientRect();
      const yesRect   = yesBtn.getBoundingClientRect();

      const minTop = titleRect.bottom + TOP_MARGIN;

      if (yesRect.top < minTop) {
        const shift = minTop - yesRect.top;
        yesBtn.style.top = (yesBtn.offsetTop + shift) + "px";
      }
    }

    function keepNoAway() {
      const forbiddenTop = title.getBoundingClientRect().bottom + TOP_MARGIN;

      const yesRect = yesBtn.getBoundingClientRect();
      const noRect  = noBtn.getBoundingClientRect();

      const overlapsYes = !(
        yesRect.right < noRect.left ||
        yesRect.left  > noRect.right ||
        yesRect.bottom < noRect.top ||
        yesRect.top > noRect.bottom
      );

      if (overlapsYes || noRect.top < forbiddenTop) {
        moveNo();
      }
    }

    function moveNo() {
      const forbiddenTop = title.getBoundingClientRect().bottom + TOP_MARGIN;

      const maxX = window.innerWidth - noBtn.offsetWidth - 20;
      const maxY = window.innerHeight - noBtn.offsetHeight - 20;

      let x, y, tries = 0;

      do {
        x = Math.random() * maxX;
        y = forbiddenTop + Math.random() * (maxY - forbiddenTop);

        noBtn.style.left = x + "px";
        noBtn.style.top  = y + "px";

        tries++;
      } while (tries < 30);
    }

    noBtn.addEventListener("click", growYes);

    yesBtn.addEventListener("click", async () => {
      await fetch("/yes", { method: "POST" });

      sound.currentTime = 105;
      sound.play().catch(() => {});

      yesBtn.style.display = "none";
      noBtn.style.display  = "none";
      gif.style.display = "none";
      img.style.display    = "block";
    });
  </script>

</body>
</html>
"""


@app.get("/")
def index():
    return HTML


@app.post("/yes")
def yes():
    return "Gut so! 🎉"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
