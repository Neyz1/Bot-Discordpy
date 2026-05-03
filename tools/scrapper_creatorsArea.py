# VIBE CODEE





import json
import time
import requests
from dataclasses import dataclass, field
from datetime import datetime

# --- Config ---
KEYWORDS = []
BASE_URL = "https://creatorsarea.fr/api/offers"
TARGET_CATEGORIES = ["DEVELOPER", "TEAM", "DESIGNER", "EDITOR"]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
}
KIND_LABELS = {
    "DEVELOPER": "Développeur",
    "DESIGNER":  "Graphiste",
    "EDITOR":    "Monteur vidéo",
    "TEAM":      "Équipe",
}

# --- Dataclass ---
@dataclass
class JobOffer:
    title:       str
    company:     str
    location:    str
    url:         str
    source:      str
    description: str = ""
    tags:        list[str] = field(default_factory=list)
    posted_at:   str = ""
    scraped_at:  str = field(default_factory=lambda: datetime.now().isoformat())


# --- Scraper ---
def fetch_jobs() -> list[JobOffer]:
    jobs = []

    for category in TARGET_CATEGORIES:
        print(f"[CreatorsArea] Scraping : {category}")

        try:
            resp = requests.get(BASE_URL, headers=HEADERS, params={"category": category}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            print(f"[CreatorsArea] Erreur ({category}) : {e}")
            continue

        offers = data.get("results", [])
        for offer in offers:
            if KEYWORDS and not matches_keywords(offer):
                continue
            job = parse_offer(offer)
            if job:
                jobs.append(job)

        time.sleep(1)

    return jobs


def parse_offer(offer: dict) -> JobOffer | None:
    try:
        slug       = offer.get("slug", "")
        title      = offer.get("title", "").strip()
        kind       = offer.get("kind", "")
        content    = offer.get("content", "")
        created_at = offer.get("createdAt", "")
        pricing    = offer.get("pricing", {})
        tags       = [t.get("name", "") for t in offer.get("_tags", []) if t.get("name")]

        is_volunteer = pricing.get("volunteer", False)
        budget       = pricing.get("value", 0)
        budget_str   = "Bénévolat" if is_volunteer else (f"{budget}€" if budget else "Non précisé")

        return JobOffer(
            title       = title,
            company     = f"Creators Area ({KIND_LABELS.get(kind, kind)}) — {budget_str}",
            location    = "Remote (France)",
            url         = f"https://creatorsarea.fr/offres/{slug}",
            source      = "creatorsarea",
            description = content[:500],
            tags        = tags,
            posted_at   = created_at,
        )
    except Exception as e:
        print(f"[CreatorsArea] Erreur parsing : {e}")
        return None


def matches_keywords(offer: dict) -> bool:
    haystack = " ".join([
        offer.get("title", ""),
        offer.get("content", ""),
        " ".join(t.get("name", "") for t in offer.get("_tags", [])),
    ]).lower()
    return any(kw.lower() in haystack for kw in KEYWORDS)


# --- Main ---
if __name__ == "__main__":
    jobs = fetch_jobs()
    print(f"\n=== {len(jobs)} offre(s) trouvée(s) ===")
    for job in jobs:
        print(f"\n  {job.title}")
        print(f"  {job.url}")
        print(f"  Tags : {', '.join(job.tags) or '—'}")
        print(f"  Publié le : {job.posted_at[:10]}")