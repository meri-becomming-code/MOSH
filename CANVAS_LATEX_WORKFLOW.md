# Canvas LaTeX Math Conversion - K-12 Teacher Guide

## 🎯 Goal: Make Math Accessible in Canvas (No Paid Tools Required)

This guide helps you convert math equations to Canvas-compatible format using **only free tools and manual work**. Optional: Use Gemini AI to speed things up.

---

## Why LaTeX in Canvas?

✅ **Students can copy/paste equations** (no retyping from images)  
✅ **Screen readers work** (accessibility for all students)  
✅ **Looks professional** on any device  
✅ **Searchable** (Ctrl+F actually finds equations)  

---

## Quick Start: Canvas LaTeX Syntax

### Inline Equations (within sentences)
Type this in Canvas:
```
The quadratic formula is \(x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\) where a ≠ 0.
```

### Display Equations (centered, own line)
Type this in Canvas:
```
$$
x^2 + 5x + 6 = 0
$$
```

**That's it!** Canvas automatically converts to beautiful math.

---

## Converting Your Existing Content

### Option 1: Manual Conversion (Simplest, Always Works)

**For digital documents** (existing Canvas pages, Word docs):
1. Look at the equation
2. Type it in LaTeX using the reference below
3. Paste into Canvas

**For handwritten solutions**:
1. Type what you see
2. Use the LaTeX Quick Reference below
3. Test in Canvas to verify it looks right

**Time estimate**: 2-3 minutes per equation initially, faster with practice

### Option 2: Use Gemini AI to Help (Optional, Faster)

If you're already using Gemini, you can have it convert for you:

**Prompt example**:
```
Convert this equation to Canvas LaTeX format:
"x squared plus 5x plus 6 equals zero"
```

**Gemini will give you**:
```
$$x^2 + 5x + 6 = 0$$
```

Then just copy/paste into Canvas!

**For handwritten notes**: 
- Take a photo
- Upload to Gemini with: "Convert this handwritten equation to Canvas LaTeX"
- Copy the result

### Option 3: Use the Automated Script (Tech-Savvy Teachers)

If you have existing HTML files, run:
```powershell
python latex_converter.py "path\to\your\files"
```

This auto-converts text equations and analyzes images. See technical docs for details.

---

## LaTeX Quick Reference for K-12 Math

### Basic Operations
| You Want | You Type | Result |
|----------|----------|--------|
| x squared | `x^2` or `x^{2}` | \\(x^2\\) |
| x cubed | `x^3` | \\(x^3\\) |
| 2 to the nth | `2^n` | \\(2^n\\) |
| x subscript 1 | `x_1` | \\(x_1\\) |

### Fractions
| You Want | You Type | Result |
|----------|----------|--------|
| One half | `\frac{1}{2}` | \\(\frac{1}{2}\\) |
| 3 over 4 | `\frac{3}{4}` | \\(\frac{3}{4}\\) |
| a over b | `\frac{a}{b}` | \\(\frac{a}{b}\\) |

### Roots & Radicals
| You Want | You Type | Result |
|----------|----------|--------|
| Square root of x | `\sqrt{x}` | \\(\sqrt{x}\\) |
| Cube root of 8 | `\sqrt[3]{8}` | \\(\sqrt[3]{8}\\) |
| Square root of 2x+1 | `\sqrt{2x+1}` | \\(\sqrt{2x+1}\\) |

### Symbols
| You Want | You Type | Result |
|----------|----------|--------|
| Less than or equal | `\le` | \\(\le\\) |
| Greater than or equal | `\ge` | \\(\ge\\) |
| Not equal | `\ne` | \\(\ne\\) |
| Plus or minus | `\pm` | \\(\pm\\) |
| Approximately | `\approx` | \\(\approx\\) |
| Infinity | `\infty` | \\(\infty\\) |
| Pi | `\pi` | \\(\pi\\) |
| Theta | `\theta` | \\(\theta\\) |
| Degrees | `^\circ` | \\(^\circ\\) |

### Common Formulas (Copy/Paste These!)

**Quadratic Formula**:
```
$$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
```

**Pythagorean Theorem**:
```
$$a^2 + b^2 = c^2$$
```

**Slope**:
```
$$m = \frac{y_2 - y_1}{x_2 - x_1}$$
```

**Distance Formula**:
```
$$d = \sqrt{(x_2-x_1)^2 + (y_2-y_1)^2}$$
```

**Area of Circle**:
```
$$A = \pi r^2$$
```

**Volume of Cylinder**:
```
$$V = \pi r^2 h$$
```

---

## Handling Graphs & Diagrams

### Static Images (Simplest)
If you have a graph as an image:
1. Upload to Canvas
2. **Add descriptive alt text**: "Graph of y = x² showing parabola opening upward, vertex at origin"
3. Done!

### Interactive Graphs (Better for Learning)
Use **Desmos** (free, no login required):

1. Go to https://www.desmos.com/calculator
2. Type your equation (e.g., `y = x^2 - 4x + 3`)
3. Click **Share** → **Embed**
4. Copy the code
5. In Canvas: Edit page → **< >** (HTML view) → Paste
6. Save!

**Example embed code**:
```html
<iframe src="https://www.desmos.com/calculator/YOUR_ID_HERE" 
        width="100%" height="400">
</iframe>
```

Students can now zoom, trace, and interact with the graph!

---

## Step-by-Step: Converting a Worksheet

**Example**: You have a Word doc of practice problems

### Before (in Word):
```
Solve: x² - 5x + 6 = 0

Answer: x = 2 or x = 3
```

### After (in Canvas):
```
**Practice Problem 1**

Solve: $$x^2 - 5x + 6 = 0$$

<details>
<summary>Show Solution</summary>

**Step 1**: Factor the quadratic
$$x^2 - 5x + 6 = (x - 2)(x - 3)$$

**Step 2**: Set each factor to zero
$$(x - 2) = 0 \text{ or } (x - 3) = 0$$

**Answer**: \(x = 2\) or \(x = 3\)

</details>
```

**Time to convert**: 3-5 minutes

---

## Using Gemini to Speed Things Up

### Prompt Templates

**For single equations**:
```
Convert to Canvas LaTeX: "the square root of x plus 1 over 2"
```

**For multiple equations**:
```
Convert these to Canvas LaTeX format:
1. x squared plus 3x minus 4
2. the square root of 25
3. 2 pi r
```

**For handwritten work**:
```
[Upload image]
"Please convert this handwritten math to Canvas LaTeX format"
```

**For Word documents**:
```
[Paste text]
"Convert all equations in this text to Canvas LaTeX delimiters"
```

---

## Testing Your Equations

### In Canvas:
1. Create a new page
2. Type your LaTeX
3. Click **Save**
4. View the page - math should render beautifully!

### Troubleshooting:
- **Not rendering?** Check your delimiters: `\(` and `\)` for inline, `$$` for display
- **Wrong spacing?** Use `\ ` (backslash-space) for gaps
- **Fraction looks weird?** Make sure you used `\frac{top}{bottom}`

### Check Accessibility:
1. Canvas → Page → **Accessibility** checker
2. Should show ✅ for all equations
3. Test: Have someone use a screen reader

---

## Sample Workflow: Converting a Unit

Let's say you're converting "Unit 2: Quadratic Functions"

**Time budget**: 2-3 hours for a full unit (first time)

1. **📄 Create main Canvas page** (10 min)
   - Title, overview, learning objectives
   
2. **✏️ Convert equations** (60-90 min)
   - Go equation by equation
   - Use Gemini for complex ones
   - Test as you go
   
3. **📊 Add interactive graphs** (30 min)
   - Create 3-4 key Desmos graphs
   - Embed in Canvas
   
4. **♿ Accessibility check** (15 min)
   - Run Canvas checker
   - Fix any flagged issues
   - Add alt text to images
   
5. **🧪 Student test** (15 min)
   - Have a student preview
   - Check on phone and computer
   - Adjust as needed

---

## K-12 Specific Tips

### Elementary (Grades K-5)
- Mostly images are fine (fractions, number lines)
- Use LaTeX for: `\frac{1}{2}`, `3 \times 4`, `\div`
- Keep it simple!

### Middle School (Grades 6-8)
- Start using LaTeX for all algebraic expressions
- Exponents: `x^2`, `2^3`
- Inequalities: `x \le 5`, `y \ge 10`
- Good time to teach students to read LaTeX

### High School (Grades 9-12)
- Full LaTeX for all equations
- Interactive Desmos graphs (essential!)
- Students can learn to write simple LaTeX themselves

---

## Success Checklist

Before sharing with students:

- [ ] All equations use `\(...\)` or `$$...$$` (no equation images)
- [ ] Tested on desktop browser
- [ ] Tested on mobile phone
- [ ] Accessibility checker passed
- [ ] At least one colleague reviewed
- [ ] Graphs are clear and labeled
- [ ] Solutions are hidden in spoiler tags (optional)

---

## Getting Help

### LaTeX Not Working?
1. Copy your code
2. Paste in Desmos calculator (it uses same math syntax)
3. See if it renders there
4. Adjust and retry in Canvas

### Still Stuck?
Ask Gemini: "Why isn't this Canvas LaTeX working: [paste your code]"

### Resources
- **Practice LaTeX**: https://www.desmos.com/calculator (just start typing!)
- **Canvas Guide**: Search "Canvas equation editor" in Canvas Help
- **LaTeX Reference**: https://www.overleaf.com/learn/latex/

---

## Time Savings Over Time

**First equation**: 5 minutes  
**After 10 equations**: 2 minutes  
**After 50 equations**: 30 seconds  
**With Gemini help**: Even faster!

**Your reward**: Students who can actually use your math content, accessible to all learners, and professional-looking pages that rival textbooks.

☕ **Worth a Starbucks card? Absolutely!**
