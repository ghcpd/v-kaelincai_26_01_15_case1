"""
Simple Demo: Read and test User Agents with trailing spaces
"""

import json

print("=" * 70)
print("Issue #307 Demo: User Agent Trailing Space Problem")
print("=" * 70)

# Read browsers.json
with open('src/fake_useragent/data/browsers.json', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find UAs with trailing spaces
uas_with_space = []
for line in lines:
    try:
        data = json.loads(line.strip())
        ua = data.get('useragent', '')
        if ua.endswith(' '):
            uas_with_space.append(ua)
            if len(uas_with_space) >= 5:
                break
    except:
        pass

print(f"\nFound {len(uas_with_space)} User Agents with trailing spaces:\n")
for i, ua in enumerate(uas_with_space, 1):
    print(f"{i}. Length: {len(ua)}")
    print(f"   Content: {ua[:80]}...")
    print(f"   Trailing chars: repr={repr(ua[-5:])}")
    print()

print("=" * 70)
print("Problem Impact:")
print("=" * 70)
print("[X] These trailing spaces cause httpx library to throw exceptions")
print("[X] Affects approximately 56.4% of User Agent strings")
print("[OK] Fixed in PR #308: Remove all trailing spaces")
print("\nDetails: https://github.com/fake-useragent/fake-useragent/issues/307")
