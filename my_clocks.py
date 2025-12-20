import streamlit as st
import streamlit.components.v1 as components

def flip_clock():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {
        background: transparent;
    }

    .container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    }

    .clock {
        display: flex;
        gap: 5px;
        font-family: 'Arial Black', sans-serif;
    }
    .digit {
        background: linear-gradient(#333, #000);
        color: white;
        font-size: 30px;
        padding: 10px 14px;
        border-radius: 8px;
        box-shadow: inset 0 -4px 0 rgba(0,0,0,0.4);
    }
    .colon {
        font-size: 30px;
        color: white;
        padding-top: 10px;
    }
    </style>
    </head>

    <body>
    <div class="container">
        <div class="clock">
            <div class="digit" id="h1">0</div>
            <div class="digit" id="h2">0</div>
            <div class="colon">:</div>
            <div class="digit" id="m1">0</div>
            <div class="digit" id="m2">0</div>
            <div class="colon">:</div>
            <div class="digit" id="s1">0</div>
            <div class="digit" id="s2">0</div>
        </div>
    </div>

    <script>
    function updateClock() {
        const now = new Date();
        const h = String(now.getHours()).padStart(2,'0');
        const m = String(now.getMinutes()).padStart(2,'0');
        const s = String(now.getSeconds()).padStart(2,'0');
        const t = h + m + s;

        ["h1","h2","m1","m2","s1","s2"].forEach((id,i)=>{
            document.getElementById(id).innerText = t[i];
        });
    }

    setInterval(updateClock, 1000);
    updateClock();
    </script>
    </body> 
    </html>
    """

    components.html(html, height=120)


def digital_clock():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap');

    html, body {
        height: 100%;
        margin: 0;
    }

    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }

    /* Clock layout */
    .clock {
        background: black;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: 0 0 18px #ff9900;
        display: flex;
        align-items: center;
        font-family: 'Orbitron', monospace;
    }

    /* Digits */
    .digit {
        color: #ff9900;
        font-size: 45px;
        letter-spacing: 4px;
        text-shadow:
            0 0 6px #ff9900,
            0 0 12px #ff9900,
            0 0 18px #ff9900;
    }

    /* Colon blink */
    .colon {
        color: #ff9900;
        font-size: 30px;
        animation: blink 1s infinite;
    }

    @keyframes blink {
        50% { opacity: 0; }
    }
    </style>
    </head>

    <body>
    <div class="container">
    <div class="clock">
        <div class="digit" id="clock">00:00:00</div>
    </div>
    </div>

    <script>
    function updateClock() {
        const now = new Date();
        const h = String(now.getHours()).padStart(2, '0');
        const m = String(now.getMinutes()).padStart(2, '0');
        const s = String(now.getSeconds()).padStart(2, '0');
        document.getElementById("clock").innerText = `${h}:${m}:${s}`;
    }

    setInterval(updateClock, 1000);
    updateClock();
    </script>
    </body>
    </html>
    """

    components.html(html, height=160)