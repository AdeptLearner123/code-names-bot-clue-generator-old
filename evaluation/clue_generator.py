from code_names_bot_clue_generator.clues.clues_database import CluesDatabase

class ClueGenerator:
    def __init__(self, clue_database_path):
        self.clues_database = CluesDatabase(clue_database_path)
        
    def get_best_clue(self, pos_terms, neg_terms, ignore=[]):
        top_clues = self.get_top_clues(pos_terms, neg_terms, 1, ignore)
        if len(top_clues) == 0:
            return None, None, None, None, None
        return top_clues[0]

    def get_top_clues(self, pos_terms, neg_terms, count, ignore=[]):
        term_to_clues = self._get_term_to_clues(pos_terms, neg_terms)
        neg_scores = self._get_clue_neg_scores(neg_terms, term_to_clues)
        clue_scores, clue_counts, clue_terms = self._aggregate_clues(
            pos_terms, neg_scores, term_to_clues
        )
        clue_reasons = self._get_clue_reasons(term_to_clues)
        return self._get_sorted_clues(clue_scores, clue_counts, clue_terms, clue_reasons, count, ignore)

    def _get_sorted_clues(self, clue_scores, clue_counts, clue_terms, clue_reasons, count, ignore=[]):
        clue_scores_list = []
        for clue in clue_scores:
            if clue not in ignore:
                clue_scores_list.append(
                    (clue, clue_scores[clue], clue_counts[clue], clue_terms[clue], clue_reasons[clue])
                )
        clue_scores_list.sort(key=lambda tup: tup[1], reverse=True)

        return clue_scores_list[:count]

    def _get_term_to_clues(self, pos_terms, neg_terms):
        term_to_clues = {}
        for term in pos_terms + neg_terms:
            term_to_clues[term] = self.clues_database.get_all_clues(term)
        return term_to_clues

    def _aggregate_clues(self, pos_terms, neg_scores, term_to_clues):
        clue_scores = {}
        clue_counts = {}
        clue_terms = {}
        for term in pos_terms:
            term_clues = term_to_clues[term]
            for clue in term_clues:
                clue_score, _, _ = term_clues[clue]
                if clue in neg_scores and neg_scores[clue] >= clue_score:
                    continue
                if clue not in clue_scores:
                    clue_scores[clue] = 0
                    clue_counts[clue] = 0
                    clue_terms[clue] = []
                clue_scores[clue] += clue_score
                clue_counts[clue] += 1
                clue_terms[clue].append(term)
        return clue_scores, clue_counts, clue_terms

    def _get_clue_neg_scores(self, neg_terms, term_to_clues):
        neg_scores = {}
        for neg_term in neg_terms:
            neg_clues = term_to_clues[neg_term]
            for neg_clue in neg_clues:
                neg_score, _, _ = neg_clues[neg_clue]
                if neg_clue not in neg_scores:
                    neg_scores[neg_clue] = neg_score
                else:
                    neg_scores[neg_clue] = max(
                        neg_scores[neg_clue], neg_score
                    )
        return neg_scores

    def _get_clue_reasons(self, term_to_clues):
        clue_reasons = {}

        for term in term_to_clues:
            term_clues = term_to_clues[term]
            for clue in term_clues:
                _, clue_type, clue_reason = term_clues[clue]
                
                if clue not in clue_reasons:
                    clue_reasons[clue] = {}
                
                clue_reasons[clue][term] = {
                    "type": clue_type,
                    "reason": clue_reason
                }

        return clue_reasons