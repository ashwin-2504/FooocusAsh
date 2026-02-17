import os
import re

def verify_file_content(filepath, patterns, negative_patterns=[]):
    if not os.path.exists(filepath):
        print(f"[FAIL] File not found: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_passed = True
    for name, pattern in patterns:
        if re.search(pattern, content):
            print(f"[PASS] {name} found in {filepath}")
        else:
            print(f"[FAIL] {name} NOT found in {filepath}")
            all_passed = False
            
    for name, pattern in negative_patterns:
        if re.search(pattern, content):
            print(f"[FAIL] {name} SHOULD NOT BE in {filepath} but was found")
            all_passed = False
        else:
            print(f"[PASS] {name} correctly removed from {filepath}")
            
    return all_passed

def run_verification():
    print("--- Verifying Lean Engine Transformation ---\n")
    
    # 1. Verify UUID Filenames (Phase 2) in async_worker.py
    print("Checking Phase 2: Static Asset Delivery (async_worker.py)")
    verify_file_content('modules/async_worker.py', [
        ("UUID Import", r"import uuid"),
        ("UUID Filename Generation", r"filename = f\"\{uuid.uuid4\(\)\}.png\""),
        ("Save to TMP", r"tmp_dir = os.path.join\(\"outputs\", \"tmp\"\)")
    ])
    
    # 2. Verify Adaptive Gating (Phase 3) in webui.py
    print("\nChecking Phase 3: Loop Optimization (webui.py)")
    verify_file_content('webui.py', [
        ("10Hz Throttler", r"if current_time - last_yield_time < 0.1:"),
        ("Sleep Increase", r"time.sleep\(0.02\)")
    ], [
        ("Intermediate Yield Loop", r"async_task.yields.append\(\['preview', ...\]\)") 
    ])
    
    # 3. Verify De-Bloating (Phase 4)
    print("\nChecking Phase 4: De-Bloating (webui.py, script.js)")
    verify_file_content('webui.py', [], [
        ("zoom.js injection", r"javascript/zoom.js")
    ])
    verify_file_content('javascript/script.js', [], [
        ("Global MutationObserver", r"mutationObserver.observe\(gradioApp\(\)"), 
        ("Style Overlay", r"initStylePreviewOverlay")
    ])

    # 4. Verify Style Whitelist (Phase 5) in sdxl_styles.py
    print("\nChecking Phase 5: Data Reduction (modules/sdxl_styles.py)")
    verify_file_content('modules/sdxl_styles.py', [
         ("Style Whitelist", r"style_whitelist = \[")
    ])

if __name__ == "__main__":
    run_verification()
