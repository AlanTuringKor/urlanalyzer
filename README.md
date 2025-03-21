

# 🔎 url_analyzer

**`url_analyzer`** is a simple utility I built to quickly **analyze a bulk list of URLs** — especially useful after running tools like `gau`, `waybackurls`, or any subdomain enumeration that produces lots of endpoints.

It extracts and summarizes:
- 🏷️ Unique domains/subdomains
- 📂 Subdirectories (with optional depth filtering)
- ❓ Query parameters (with frequency)

---

## 💡 Why?

When you're deep into a Bug Bounty session and you've got **thousands of URLs** dumped from tools like:

```bash
gau target.com > urls.txt
```

…it's hard to make sense of them all. This script breaks it down so you can:

- Prioritize interesting subdomains
- Focus on juicy directories (`/admin`, `/api`, etc.)
- Spot common query parameters like `id`, `file`, `url`, etc.

---

## ⚙️ Usage

```bash
python url_analyzer.py urls.txt -o output.txt -d 2
```

- `urls.txt`: Your file with raw URLs (one per line)
- `-o output.txt`: Optional — saves a summary and breakdown files
- `-d 2`: Optional — filters subdirectories to depth (e.g. `/foo/bar`, but not `/foo/bar/baz`)

---

## 📁 Output

If you specify `-o output.txt`, the following files will be saved:

| File                     | Description                             |
|--------------------------|-----------------------------------------|
| `output.txt`             | Full summary (domains, subdirs, params) |
| `output_subdomains.txt`  | Unique subdomains/domains               |
| `output_subdirs.txt`     | Unique subdirectory paths               |
| `output_params.txt`      | Query parameters with occurrence count  |

---

## 📘 Example

**Input (`urls.txt`)**
```
https://sub.example.com/api/user?id=1
https://test.example.com/admin/login?redirect=/dashboard
https://example.com/assets/js/main.js
```

**Command**
```bash
python url_analyzer.py urls.txt -o recon_summary.txt -d 1
```

**Output (console + files)**

```
### Unique Domains (Subdomains) ###
example.com
sub.example.com
test.example.com

### Unique Subdirectories (Depth: 1) ###
/admin
/api
/assets

### Unique Parameters ###
id (1 occurrences)
redirect (1 occurrences)
```

---

## 🧠 Notes

- Depth filtering is useful when you want to focus on top-level paths only (e.g. `/admin`, not `/admin/user/settings`)
- Parameter count gives you a sense of what’s commonly passed around (useful for guessing IDOR, SSRF, etc.)
- No external dependencies — just Python stdlib

---

## 🧑‍💻 For Bug Bounty Hunters

Combine with:

```bash
gau target.com | grep -v '\.png\|\.jpg\|\.css\|\.js' > urls.txt
python url_analyzer.py urls.txt -o summary.txt -d 2
```

Boom. Instant recon overview.

