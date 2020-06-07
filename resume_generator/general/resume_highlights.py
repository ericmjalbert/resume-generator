import os
from sklearn.metrics.pairwise import cosine_similarity

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # This removes debugging notes from tensorflow
import tensorflow_hub as hub  # noqa: E402


def get_cosine_similarity(target, list_of_vectors):
    """Returns only list of similarities for given target vector."""
    all_similarties = cosine_similarity([target[0], *list_of_vectors])
    return list(all_similarties[0])


class ResumeHighlights:
    """Holds the highlights and score for a given set of highlights.

    Has a class attribute of the embed model so that it only needs to be
    loaded once.

    Data Struct is like:
    - Section
        - ResumeHighlight (list of all highligts)
            - highlight (text)
            - score (float)
    """

    def __init__(self, highlight_mapping, job_bullets):
        self.highlight_mapping = highlight_mapping
        self.job_bullets = job_bullets

        self.resume_highlights = self._get_resume_highlights()

    def _get_resume_highlights(self):
        resume_highlights = {}
        for section, highlights in self.highlight_mapping.items():
            score_highlight_pairs = []
            for highlight in highlights:
                score_highlight_pairs.append(
                    ResumeHighlight(highlight, self.job_bullets)
                )
            resume_highlights[section] = score_highlight_pairs
        return resume_highlights

    def get_top_n_scores_in_section(self, section_id, n):
        """For the given name return the text for the top n scores in a given section."""
        top_picks = []

        highlights = self.resume_highlights[section_id]
        while len(top_picks) < n and len(highlights) > 0:
            max_highlight_index = highlights.index(max(highlights))
            selected = highlights.pop(max_highlight_index)
            top_picks.append(selected.highlight)

        return top_picks


class ResumeHighlight:
    """Given the individual highlight text it generates the score."""

    embed = hub.load("./library/universal-sentence-encoder/")

    def __init__(self, highlight, job_bullets):
        self.highlight = highlight
        self.highlight_embedding = ResumeHighlight.embed([highlight])
        self.job_embeddings = ResumeHighlight.embed(job_bullets)

        self.score = self._get_highlight_score()

    def _get_highlight_score(self):
        """The business logic for calculating how to score each highlight.

        Currently we assign the score as the sum of positive cosine_similarities.
        """
        similarities = get_cosine_similarity(
            self.highlight_embedding, self.job_embeddings
        )
        score = sum([value for value in similarities if 0 < value < 1])
        return score

    # Need all rich comparison methods to use max
    def __eq__(self, other):
        return self.score == other.score

    def __ne__(self, other):
        return self.score != other.score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score
