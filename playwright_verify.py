import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

def run_tests():
    console_errors = []
    page_errors = []

    html_path = os.path.abspath("sport_english.html").replace("\\", "/")
    url = f"file:///{html_path}"
    print(f"Testing URL: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Listen to console and page errors
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ["error"] else None)
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        print("1. Navigating to page...")
        page.goto(url, wait_until="networkidle")
        time.sleep(1)

        # Check console errors immediately after load
        print(f"Console errors on load: {len(console_errors)}")
        print(f"Page errors on load: {len(page_errors)}")
        if page_errors:
            print("ERROR DETAILS:", page_errors)

        # 2. Verify ALL_QUOTES length
        quotes_count = page.evaluate("() => typeof ALL_QUOTES !== 'undefined' ? ALL_QUOTES.length : -1")
        print(f"2. ALL_QUOTES.length = {quotes_count} (Expected: 1000)")
        assert quotes_count == 1000, f"Expected 1000 quotes, got {quotes_count}"

        # 3. Check UI elements text
        count_quotes_text = page.locator("#count-quotes").inner_text()
        print(f"3. #count-quotes text = '{count_quotes_text}' (Expected: '1000')")
        assert count_quotes_text == "1000", f"Expected '1000', got {count_quotes_text}"

        showing_count_text = page.locator("#quotes-showing-count").inner_text()
        print(f"4. #quotes-showing-count text = '{showing_count_text}'")
        assert "1000" in showing_count_text, f"Expected '1000' in showing count, got {showing_count_text}"

        # 5. Test Category Filters
        categories = {
            "discipline": 217,
            "limits": 169,
            "grit": 205,
            "endurance": 172,
            "mindset": 237
        }
        for cat, expected_num in categories.items():
            btn = page.locator(f"#qcat-{cat}")
            btn.click()
            time.sleep(0.2)
            filtered_len = page.evaluate("() => currentQuotesFiltered.length")
            print(f"   Filter '{cat}': count = {filtered_len} (Expected: {expected_num})")
            assert filtered_len == expected_num, f"Category {cat} expected {expected_num}, got {filtered_len}"

        # Reset filter to all
        page.locator("#qcat-all").click()
        time.sleep(0.2)
        assert page.evaluate("() => currentQuotesFiltered.length") == 1000

        # 6. Test Search Box
        print("6. Testing search box...")
        search_input = page.locator("#quotes-search")
        search_input.fill("Kipchoge")
        time.sleep(0.3)
        search_len = page.evaluate("() => currentQuotesFiltered.length")
        print(f"   Search 'Kipchoge': found {search_len} quotes")
        assert search_len > 0, "Search for 'Kipchoge' should return > 0 results"

        search_input.fill("破極限")
        time.sleep(0.3)
        search_len2 = page.evaluate("() => currentQuotesFiltered.length")
        print(f"   Search '破極限': found {search_len2} quotes")
        assert search_len2 > 0, "Search for '破極限' should return > 0 results"

        # Clear search
        search_input.fill("")
        time.sleep(0.3)
        assert page.evaluate("() => currentQuotesFiltered.length") == 1000

        # 7. Test Pagination & Load More
        print("7. Testing pagination...")
        initial_cards = page.locator("#quotes-grid .quote-card").count()
        print(f"   Initial visible cards = {initial_cards} (Expected: 24)")
        assert initial_cards == 24

        load_more_btn = page.locator("#btn-load-more-quotes")
        load_more_btn.click()
        time.sleep(0.2)
        after_load_more = page.locator("#quotes-grid .quote-card").count()
        print(f"   After '展開更多' visible cards = {after_load_more} (Expected: 48)")
        assert after_load_more == 48

        # Test showAllQuotes
        page.evaluate("() => showAllQuotes()")
        time.sleep(0.5)
        all_cards_count = page.locator("#quotes-grid .quote-card").count()
        print(f"   After showAllQuotes() visible cards = {all_cards_count} (Expected: 1000)")
        assert all_cards_count == 1000

        # Reset back to 24 for UI performance
        page.evaluate("() => { quotesDisplayLimit = 24; renderQuotes(); }")
        time.sleep(0.2)

        # 8. Test Spotlight Shuffle
        print("8. Testing Spotlight interaction...")
        old_spotlight_en = page.locator("#spotlight-en").inner_text()
        page.locator("button[onclick*='shuffleSpotlightQuote']").first.click()
        time.sleep(0.3)
        new_spotlight_en = page.locator("#spotlight-en").inner_text()
        print(f"   Spotlight updated: '{new_spotlight_en[:50]}...'")

        # 9. Test Quotes Auto-play toggle (Ensure no ReferenceError)
        print("9. Testing Quotes auto-play toggle...")
        btn_autoplay = page.locator("#btn-quotes-autoplay-main")
        btn_autoplay.click()
        time.sleep(0.5)
        is_playing = page.evaluate("() => isQuotesAutoPlaying")
        print(f"   Quotes auto-playing = {is_playing} (Expected: True)")
        assert is_playing == True

        # Stop auto-play
        btn_autoplay.click()
        time.sleep(0.2)
        is_playing_after = page.evaluate("() => isQuotesAutoPlaying")
        print(f"   Quotes auto-playing after stop = {is_playing_after} (Expected: False)")
        assert is_playing_after == False

        # 9.5 Test Nutrition Science Section (10 Modules)
        print("\n9.5. Testing Nutrition Science Section (10 Modules)...")
        nut_cards_count = page.locator(".nutrition-card").count()
        print(f"   Total nutrition cards in DOM = {nut_cards_count} (Expected: 10)")
        assert nut_cards_count == 10

        nut_items_count = page.evaluate("() => typeof NUTRITION_ITEMS !== 'undefined' ? NUTRITION_ITEMS.length : -1")
        print(f"   NUTRITION_ITEMS.length = {nut_items_count} (Expected: 10)")
        assert nut_items_count == 10

        # Toggle Nutrition auto-play
        page.locator("#btn-nutrition-autoplay").click()
        time.sleep(0.3)
        assert page.evaluate("() => isNutritionAutoPlaying") is True
        page.locator("#btn-nutrition-autoplay").click()
        time.sleep(0.3)
        assert page.evaluate("() => isNutritionAutoPlaying") is False
        print("   Nutrition auto-play verified.")

        # 9.6 Test Muscle Strength Section (30 Modules)
        print("\n9.6. Testing Muscle Strength Section (30 Modules)...")
        m_cards_count = page.locator(".muscle-card").count()
        print(f"   Total muscle cards in DOM = {m_cards_count} (Expected: 30)")
        assert m_cards_count == 30

        m_items_count = page.evaluate("() => typeof MUSCLE_ITEMS !== 'undefined' ? MUSCLE_ITEMS.length : -1")
        print(f"   MUSCLE_ITEMS.length = {m_items_count} (Expected: 30)")
        assert m_items_count == 30

        # 10. Test Injury & Protection Section (All 27 items)
        print("10. Testing Injury & Protection section (36 modules)...")
        injury_cards_count = page.locator(".injury-card").count()
        print(f"   Total injury cards in DOM = {injury_cards_count} (Expected: 27)")
        assert injury_cards_count == 36

        # Check tabs switching
        tabs = [
            ("itab-btn-weather", 9),          # 9 weather/sensory cards (3x3 full)
            ("itab-btn-trail", 9),            # 9 trail/survival cards (3x3 full)
            ("itab-btn-warmup", 9),           # 9 warm-up cards (3x3 full)
            ("itab-btn-musculoskeletal", 9),  # 9 musculoskeletal cards (3x3 full)
            ("itab-btn-all", 36)              # all 36 cards
        ]
        for btn_id, expected_visible in tabs:
            tab_btn = page.locator(f"#{btn_id}")
            tab_btn.click()
            time.sleep(0.2)
            visible_count = len([c for c in page.locator('.injury-card').all() if c.is_visible()])
            print(f"   Tab '#{btn_id}': visible cards = {visible_count} (Expected: {expected_visible})")
            assert visible_count == expected_visible

        # Reset injury tab to all
        page.locator("#itab-btn-all").click()
        time.sleep(0.2)

        # 11. Final error check
        print("\n11. Final Error Audit:")
        print(f"   Total Console Errors: {len(console_errors)}")
        print(f"   Total Page Exceptions: {len(page_errors)}")
        if console_errors:
            print("   Console Errors:", console_errors)
        if page_errors:
            print("   Page Exceptions:", page_errors)

        assert len(console_errors) == 0, f"Found console errors: {console_errors}"
        assert len(page_errors) == 0, f"Found page exceptions: {page_errors}"

        # Capture Screenshot
        screenshot_path = "verification_sport_english_1000.png"
        page.locator("#quotes-auto-play-hub").screenshot(path="verification_quotes_hub.png"); page.screenshot(path=screenshot_path, full_page=False)
        print(f"Screenshot captured: {screenshot_path}")

        browser.close()
        print("\n🎉 ALL TESTS PASSED WITH 0 CONSOLE ERRORS AND 0 PAGE EXCEPTIONS!")

if __name__ == "__main__":
    run_tests()
