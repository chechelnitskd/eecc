import argparse

import pandas as pd


def get_data(path):
    df = pd.read_csv(path, sep="\t", header=None)
    df.columns = ["0", "1"]
    data = {}
    for _, row in df.iterrows():
        data_type = row["0"]
        if data_type not in data:
            data[data_type] = []
        data[data_type].append(row["1"])
    return data


def get_templates(path):
    with open(path, "r") as f:
        templates = f.readlines()
    return [template.strip() for template in templates]


def handle_vowels(template, identity):
    """Handles vowels preceding identity terms in templates."""
    if "{vowel}" not in template:
        return template
    if identity[0] in ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]:
        template = template.replace("{vowel}", "an")
    else:
        template = template.replace("{vowel}", "a")
    return template


def create_prompts(concepts, identities, gender, language, templates):
    """Creates prompts from series of templates, identities, and concepts."""
    prompts = []
    for template in templates:
        for topic in concepts:
            for concept in concepts[topic]:
                for granularity in identities:
                    for identity in identities[granularity]:
                        for g in gender:
                            for gen in gender[g]:
                                for l in language:
                                    for lan in language[l]:
                                        prompt = template.split("\t")[-1].replace("{concept}", concept)
                                        prompt = prompt.split("\t")[-1].replace("{identity}", identity)
                                        prompt = prompt.split("\t")[-1].replace("{gender}", gen)
                                        prompt = prompt.split("\t")[-1].replace("{language}", lan)
                                        prompt = handle_vowels(prompt, identity)
                                        prompts.append(
                            (
                                template.split("\t")[0],
                                template.split("\t")[1],
                                template.split("\t")[2],
                                topic,
                                concept,
                                granularity,
                                identity,
                                g,
                                gen,
                                l,
                                lan,
                                prompt,
                            )
                        )
    return prompts


def main(concepts_path, identity_path, gender_path, language_path, templates_path, output_path):
    concepts = get_data(concepts_path)
    identities = get_data(identity_path)
    gender = get_data(gender_path)
    language = get_data(language_path)
    templates = get_templates(templates_path)
    prompts = create_prompts(concepts, identities, gender, language, templates)
    pd.DataFrame(prompts).to_csv(
        output_path,
        sep="\t",
        header=[
            "_",
            "_",
            "template",
            "topic",
            "concept",
            "granularity", #change this
            "identity",
            "g",
            "gen",
            "l",
            "lan",
            "prompt",
        ],
        index=None,
    )
    return


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--concepts", help="Path to concepts.tsv", type=str, default="/Users/dan/Downloads/eecc/data/stories/concepts.tsv"
    )
    argparser.add_argument(
        "--identities",
        help="Path to identities.tsv",
        type=str,
        default="/Users/dan/Downloads/eecc/data/multilingual_identities.tsv",
    )
    argparser.add_argument(
        "--templates", help="Path to templates.txt", type=str, default="/Users/dan/Downloads/eecc/data/stories/multilingual_templates.tsv"
    )
    argparser.add_argument(
        "--gender", help="Path to gender.txt", type=str, default="/Users/dan/Downloads/eecc/data/gender.tsv"
    )
    argparser.add_argument(
        "--languages", help="Path to languages.txt", type=str, default="/Users/dan/Downloads/eecc/data/languages.tsv"
    )
    argparser.add_argument(
        "--output", help="Path to prompts.tsv", type=str, default="/Users/dan/Downloads/eecc/data/stories/multilingual_prompts.tsv"
    )
    args = argparser.parse_args()
    print(args)
    main(args.concepts, args.identities, args.gender, args.languages, args.templates, args.output)
