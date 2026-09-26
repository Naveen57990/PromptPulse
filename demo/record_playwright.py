#!/usr/bin/env python3
"""
Playwright Automated Demo Video Recorder for PromptPulse Studio.
Records 1920x1080 30fps screen video with Recordly-style subtitle badges injected directly into DOM.
"""

import os
import sys
import json
import asyncio
from playwright.async_api import async_playwright

DEMO_DIR = os.path.dirname(__file__)
RAW_VIDEO_DIR = os.path.join(DEMO_DIR, "raw_video")
WEB_DIR = os.path.abspath(os.path.join(DEMO_DIR, "..", "web"))
SCRIPT_FILE = os.path.join(DEMO_DIR, "voiceover_script.json")

# Clean existing webm files in raw_video
for f in os.listdir(RAW_VIDEO_DIR):
    if f.endswith(".webm"):
        os.remove(os.path.join(RAW_VIDEO_DIR, f))

with open(SCRIPT_FILE, "r", encoding="utf-8") as f:
    SEGMENTS = json.load(f)

# Scene durations corresponding to each audio segment
DURATIONS = {
    1: 9.36,
    2: 7.46,
    3: 8.76,
    4: 8.71,
    5: 11.47,
    6: 14.50,
    7: 11.74,
    8: 10.44,
    9: 10.97,
    10: 11.54
}

async def record():
    os.makedirs(RAW_VIDEO_DIR, exist_ok=True)
    html_url = f"file://{os.path.join(WEB_DIR, 'index.html')}"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,
            record_video_dir=RAW_VIDEO_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )

        page = await context.new_page()
        await page.goto(html_url, wait_until="networkidle")

        # Inject professional Recordly-style Subtitle Badge into DOM
        await page.evaluate("""() => {
            const badge = document.createElement('div');
            badge.id = 'demoSubtitleBadge';
            badge.style.cssText = `
                position: fixed;
                bottom: 36px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(11, 15, 25, 0.94);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.18);
                border-radius: 9999px;
                padding: 12px 34px;
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 20px;
                font-weight: 600;
                color: #FFFFFF;
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7), 0 0 20px rgba(79, 70, 229, 0.25);
                z-index: 10000;
                transition: opacity 200ms ease, transform 200ms ease;
                pointer-events: none;
                text-align: center;
                max-width: 85%;
                letter-spacing: -0.01em;
            `;
            document.body.appendChild(badge);
            window.setSubtitle = (text) => {
                badge.textContent = text;
            };
        }""")

        print("🎬 Scene 1: Hook & Pain Point (9.36s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[0]['subtitle'])})")
        await page.mouse.move(960, 50)
        await page.wait_for_timeout(3000)
        await page.mouse.move(500, 180)
        await page.wait_for_timeout(3000)
        await page.mouse.move(1400, 180)
        await page.wait_for_timeout(3360)

        print("🎬 Scene 2: The Hidden Production Cost (7.46s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[1]['subtitle'])})")
        await page.mouse.move(600, 180) # Hover over Token Consumption Delta
        await page.wait_for_timeout(2000)
        await page.mouse.move(950, 180) # Hover over Cost Savings
        await page.wait_for_timeout(2000)
        await page.mouse.move(1300, 180) # Hover over Schema Integrity
        await page.wait_for_timeout(3460)

        print("🎬 Scene 3: Solution - Introducing PromptPulse Studio (8.76s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[2]['subtitle'])})")
        await page.mouse.move(1350, 45) # Hover over Deterministic Engine Active badge
        await page.wait_for_timeout(3500)
        await page.evaluate("window.scrollBy({top: 220, behavior: 'smooth'})")
        await page.wait_for_timeout(5260)

        print("🎬 Scene 4: Local-First Workbench Architecture (8.71s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[3]['subtitle'])})")
        await page.evaluate("window.scrollBy({top: 320, behavior: 'smooth'})")
        await page.wait_for_timeout(4000)
        await page.mouse.move(500, 480)
        await page.wait_for_timeout(4710)

        print("🎬 Scene 5: Side-by-side prompt editing & tokens (11.47s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[4]['subtitle'])})")
        await page.click("#promptB")
        await page.wait_for_timeout(1500)
        await page.keyboard.press("End")
        await page.keyboard.type("\nEnsure {{compliance_tier}} is verified.")
        await page.wait_for_timeout(4000)
        await page.mouse.move(1400, 720) # Hover over updated variable chips
        await page.wait_for_timeout(5970)

        print("🎬 Scene 6: Multi-Model Economics & Volume Toggle (14.50s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[5]['subtitle'])})")
        await page.evaluate("window.scrollTo({top: 140, behavior: 'smooth'})")
        await page.wait_for_timeout(2500)
        await page.mouse.move(400, 380) # Hover GPT-4o
        await page.wait_for_timeout(2500)
        await page.mouse.move(750, 380) # Hover Claude 3.5 Sonnet
        await page.wait_for_timeout(2500)
        await page.select_option("#volumeSelect", "5000000") # Toggle to 5M queries
        await page.wait_for_timeout(3500)
        await page.select_option("#volumeSelect", "1000000") # Toggle back to 1M queries
        await page.wait_for_timeout(3500)

        print("🎬 Scene 7: Run Evaluation Suite & Test Matrix (11.74s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[6]['subtitle'])})")
        await page.evaluate("window.scrollTo({top: 880, behavior: 'smooth'})")
        await page.wait_for_timeout(1500)
        await page.click("#runAllBtn") # Click Run Evaluation Suite
        await page.wait_for_timeout(2500)
        await page.click(".test-card:first-child .test-card-header") # Expand test card 1
        await page.wait_for_timeout(3500)
        await page.click(".filter-btn[data-filter='pass']") # Filter Pass
        await page.wait_for_timeout(2000)
        await page.click(".filter-btn[data-filter='all']") # Filter All
        await page.wait_for_timeout(2240)

        print("🎬 Scene 8: Interactive Custom Test Modal (10.44s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[7]['subtitle'])})")
        await page.click("#addTestCaseBtn") # Open modal
        await page.wait_for_timeout(1500)
        await page.fill("#newTestName", "Multi-Currency Global Refund")
        await page.wait_for_timeout(1000)
        await page.fill("#newTestDesc", "Verifies EUR/GBP currency code retention in JSON response.")
        await page.wait_for_timeout(2000)
        await page.click("#saveCustomTestBtn") # Save & Run
        await page.wait_for_timeout(5940)

        print("🎬 Scene 9: CLI & Pytest Verification (10.97s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[8]['subtitle'])})")
        await page.evaluate("window.scrollTo({top: 1450, behavior: 'smooth'})")
        await page.wait_for_timeout(5000)
        await page.evaluate("window.scrollTo({top: 600, behavior: 'smooth'})")
        await page.wait_for_timeout(5970)

        print("🎬 Scene 10: Export Report & Outro (11.54s)")
        await page.evaluate(f"window.setSubtitle({json.dumps(SEGMENTS[9]['subtitle'])})")
        await page.evaluate("window.scrollTo({top: 0, behavior: 'smooth'})")
        await page.wait_for_timeout(2000)
        await page.click("#exportReportBtn") # Click export
        await page.wait_for_timeout(3500)
        await page.mouse.move(960, 540)
        await page.wait_for_timeout(6040)

        # Close
        await page.close()
        video_path = await page.video.path()
        await context.close()
        await browser.close()

        print(f"✅ Master high-DPI video recorded at: {video_path}")
        return video_path

if __name__ == "__main__":
    asyncio.run(record())
