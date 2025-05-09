import arxiv
import toml
import datetime

def parse_config(config_path):
    cfg = toml.load(config_path)
    return cfg

def search_arxiv(query, max_results=10, sort_by=arxiv.SortCriterion.SubmittedDate):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_by
    )
    return search

def result_to_dicts(arxiv_results):
    results = []
    for result in arxiv_results:
        result_dict = {
            "title": result.title,
            "summary": result.summary,
            "published": result.published,
            "authors": [author.name for author in result.authors],
            "doi": result.doi,
            "url": result.entry_id,
            "pdf_url": result.pdf_url
        }
        results.append(result_dict)
    return results

def to_markdown_table(columns, results):
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    rows = []

    for result in results:
        row = "| "
        for col in columns:
            if col == "authors":
                row += ", ".join(result[col]) + " | "
            else:
                row += str(result[col]) + " | "
        rows.append(row)

    return "\n".join([header, separator] + rows)

def write_to_file(content, file_path):
    with open(file_path, "w") as f:
        f.write("# Daily ArXiv\n\n")
        f.write("## Updated at " + str(datetime.datetime.now().strftime("%Y-%m-%d")) + "\n\n")
        f.write(content)

if __name__ == "__main__":
    cfg = parse_config("config.toml")

    search = search_arxiv(
        query=cfg["arxiv"]["query"],
        max_results=cfg["arxiv"]["max_results"]
    )

    results = result_to_dicts(search.results())

    md_table = to_markdown_table(
        columns=cfg["markdown"]["columns"],
        results=results
    )

    write_to_file(md_table, cfg["markdown"]["path"])