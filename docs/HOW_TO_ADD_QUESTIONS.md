# How to Add Questions and Sub-Questions

This guide explains the **easiest way** to add new questions to your coffee feedback system.

## Current System (2 Questions Only)

Your app now has a simple 2-question flow:
1. **Primary Flavor** - User selects main flavor (Fruity, Cocoa, etc.)
2. **Sub-Flavor** - Based on selection, shows specific options from CSV

---

## Easy Way: Using CSV File Only

### To Add New Sub-Questions to Existing Categories

Just edit `Flavor.csv` file:

**Example CSV Structure:**
```csv
Fruity Types,Sensory Group
Citrus fruit,Fruity
Lemon,Fruity
Orange,Fruity
Grapefruit,Fruity
Chocolate,Cocoa
Dark Chocolate,Cocoa
Milk Chocolate,Cocoa
```

**Rules:**
- Column 1: `Fruity Types` - The sub-option name
- Column 2: `Sensory Group` - The main category it belongs to
- Sub-options automatically appear under their category
- **No code changes needed!** Just edit CSV and restart backend

### To Add a New Main Category

1. **Edit `Flavor.csv`** - Add new rows with your category name in `Sensory Group` column:
   ```csv
   Fruity Types,Sensory Group
   Vanilla,Sweetness
   Caramel,Sweetness
   Honey,Sweetness
   ```

2. **Edit `backend/services.py`** - Add the category to two places:

   **Place 1:** In `QUESTION_FLOW` (around line 15):
   ```python
   "flavor_main": {
       "next_map": {
           "Fruity": "flavor_fruity",
           "Cocoa": "flavor_cocoa",
           "Sweetness": "flavor_sweetness",  # ADD NEW LINE
           ...
       }
   },
   ```

   **Place 2:** End the flow after sub-question (around line 40):
   ```python
   "flavor_fruity": {"next": None},
   "flavor_cocoa": {"next": None},
   "flavor_sweetness": {"next": None},  # ADD NEW LINE
   ```

3. **Add to main question options** (around line 95):
   ```python
   "options": ["Fruity", "Floral", "Nutty", "Cereal", "Cocoa", "Sweet", "Earthy", 
               "Roasted", "Spices", "Vegetative", "Stale/Papery", "Chemical", 
               "Sweetness",  # ADD NEW CATEGORY
               "Alcohol/Fermented", "None", "Not Applicable"],
   ```

4. **Delete database and restart:**
   ```powershell
   cd backend
   Remove-Item coffee_feedback.db
   python -m uvicorn main:app --reload
   ```

---

## Advanced Way: Add Multi-Level Questions

If you want more than 2 questions (like adding intensity, body, etc.):

### Step 1: Add Question to `questions_data` array

In `backend/services.py` (around line 100):

```python
questions_data = [
    {
        "id": "flavor_main",
        "text": "What is the primary flavor profile you detect?",
        "type": "single_choice",
        "options": ["Fruity", "Cocoa", ...],
        "category": "Flavor",
        "order_index": 1
    },
    # ADD NEW QUESTION HERE
    {
        "id": "intensity",
        "text": "How would you rate the intensity?",
        "type": "rating",
        "options": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
        "category": "Intensity",
        "order_index": 100
    }
]
```

**Question Types:**
- `single_choice` - Select one option
- `multiple_choice` - Select multiple options
- `rating` - Number scale (1-10)
- `open` - Text input

### Step 2: Add to Question Flow

In `QUESTION_FLOW` dictionary (around line 15):

```python
QUESTION_FLOW = {
    "flavor_main": {
        "next_map": {
            "Fruity": "flavor_fruity",
            "Cocoa": "flavor_cocoa",
            ...
        }
    },
    "flavor_fruity": {"next": "intensity"},  # Go to intensity after sub-flavor
    "flavor_cocoa": {"next": "intensity"},
    "intensity": {"next": None}  # End here
}
```

### Step 3: Delete Database and Restart

```powershell
cd backend
Remove-Item coffee_feedback.db -Force
.\venv\Scripts\Activate.ps1
python -m uvicorn main:app --reload
```

---

## Quick Reference

| Task | Difficulty | Files to Edit |
|------|-----------|---------------|
| Add sub-options to existing category | ⭐ Easy | `Flavor.csv` only |
| Add new main category | ⭐⭐ Medium | `Flavor.csv` + `services.py` (3 places) |
| Add follow-up questions | ⭐⭐⭐ Advanced | `services.py` (questions_data + QUESTION_FLOW) |

---

## Tips

✅ **Always delete `coffee_feedback.db` after changes** - Database caches questions
✅ **Use utf-8 encoding for CSV** - Prevents character issues
✅ **Test immediately** - Start a session and verify new questions appear
✅ **Check terminal logs** - Shows "Loading X questions into database"

## Example: Adding "Sweetness" Category

**1. Edit `Flavor.csv`:**
```csv
Fruity Types,Sensory Group
Vanilla,Sweetness
Caramel,Sweetness
Honey,Sweetness
```

**2. Edit `services.py` - Add to QUESTION_FLOW:**
```python
"Sweetness": "flavor_sweetness",  # Line ~25
```

**3. Add flow end:**
```python
"flavor_sweetness": {"next": None},  # Line ~45
```

**4. Add to main options:**
```python
"options": ["Fruity", "Cocoa", "Sweetness", ...],  # Line ~95
```

**5. Restart:**
```powershell
Remove-Item backend\coffee_feedback.db -Force
cd backend; .\venv\Scripts\Activate.ps1; python -m uvicorn main:app --reload
```

Done! ✨
