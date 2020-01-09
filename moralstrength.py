import lexicon_use
from estimators import estimate,models
import spacy
import en_core_web_sm
import math

nlp = en_core_web_sm.load()
moral_options_lexicon = ['care', 'fairness', 'loyalty', 'authority', 'purity']
moral_options_predictions = moral_options_lexicon + ['non-moral']


def word_moral_value(word,moral,normalized=False):
    """Returns the association strength between word and moral trait, 
       as rated by annotators. Value ranges from 1 to 9.
       1: words closely associated to vices: harm, cheating, betrayal, subversion, degradation
       9: words closely associated to virtues: care, fairness, loyalty, authority, sanctity
       normalized=True will normalize each annotation in the range -1 (vice) to +1 (virtue)
       If the word is not in the lexicon of that moral trait, returns NaN.
       For a list of available traits, get_available_lexicon_traits()
       """
       
    if moral not in moral_options_lexicon:
        raise ValueError('Invalid moral trait "{}" specified. Valid traits are: {}'.format(moral,moral_options_lexicon))
    moral_value = lexicon_use.moral_value(word,moral,normalized)
    return moral_value


def word_moral_annotations(word,normalized=False):
    """Returns a dict that gives the association strength between word and every 
       moral trait, as rated by annotators. Value ranges from 1 to 9.
       1: words closely associated to harm, cheating, betrayal, subversion, degradation
       9: words closely associated to care, fairness, loyalty, authority, purity/sanctity
       normalized=True will normalize each annotation in the range -1 (vice) to +1 (virtue)
       If the word is not in the lexicon of that moral trait, returns NaN."""
    return {moral: lexicon_use.moral_value(word, moral,normalized) for moral in moral_options_lexicon}


def string_average_moral(text,moral,normalized=False):
    """Returns the average of the annotations for the words in the sentence (for one moral).
       normalize=True will normalize each annotation in the range -1 (vice) to +1 (virtue)
       If no word is recognized/found in the lexicon, returns NaN.
       Text is lemmatized using spacy.
       """
    sum = 0
    import pdb
    pdb.set_trace()
    recognized_words_no = 0
    for token in nlp(text):
        lemma = token.lemma_
        value = word_moral_value(lemma,moral,normalized)
        #print("lemma: {}".format(lemma))
        if not math.isnan(value):
            sum += value
            recognized_words_no += 1
    if recognized_words_no == 0:
        return float('NaN')
    else:
        return sum/recognized_words_no



def string_vader_moral(text,moral,alpha=15):
    """Returns a normalized annotation score for the words in the sentence (for one moral).
       Score ranges from -1 (vices) to 1 (virtues) and is calculated as in VADER (Hutto and Gilbert, 2014).
       The optional alpha parameter defines how quickly the score maxes out (to 1 or -1), and can be tweaked (e.g. for very long texts it *might* be more sensible to set it to 150; 15 is the default taken from VADER).
       If no word is recognized/found in the lexicon, returns NaN.
       Text is lemmatized using spacy.
       """
    score = 0
    recognized_words_no = 0
    for token in nlp(text):
        lemma = token.lemma_
        value = word_moral_value(lemma,moral,normalized=True)
        if not math.isnan(value):
            score += value
            recognized_words_no += 1
    if recognized_words_no == 0:
        return float('NaN')
    else:
        return score/math.sqrt((score*score) + alpha)



def get_available_models():
    """Returns a list of available models for predicting texts.
       Short explanation of names:
       unigram: simple unigram-based model
       count: number of words that are rated as closer to moral extremes 
       freq: distribution of moral ratings across the text
       simon: SIMilarity-based sentiment projectiON
       or a combination of these.
       For a comprehensive explanation of what each model does and how it performs on 
       different datasets, see https://arxiv.org/abs/1904.08314 
       (currently being reviewed at Expert Systems and Application)."""
    
    return models

def get_available_lexicon_traits():
    """Returns a list of traits that were annotated and can be queried 
       by word_moral_value().
       care: Care/Harm
       fairness: Fairness/Cheating
       loyalty: Loyalty/Betrayal
       authority: Authority/Subversion
       purity: Purity/Degradation
       """
       
    return moral_options_lexicon
    
def get_available_prediction_traits():
    """Returns a list of traits that can be predicted by string_moral_value() 
       or file_moral_value().
       care: Care/Harm
       fairness: Fairness/Cheating
       loyalty: Loyalty/Betrayal
       authority: Authority/Subversion
       purity: Purity/Degradation
       non-moral: Tweet/text is non-moral
       """
       
    return moral_options_predictions

def string_moral_value(text,moral,model='unigram+freq'):
    """Returns the estimated probability that the text is relevant to either a vice or 
       virtue of the corresponding moral trait.
       The default model is unigram+freq, the best performing (on average) across all 
       dataset, according to our work.
       For a list of available models, see get_available_models(). 
       For a list of traits, get_available_prediction_traits().
    """
    
    if model not in models:
        raise ValueError('Invalid model "{}" specified. Valid models are: {}'.format(model,models))      
    if moral not in moral_options_predictions:
        raise ValueError('Invalid moral trait "{}" specified. Valid traits are: {}'.format(moral,moral_options_predictions))    
    return estimate(text, moral=moral, model=model)[0]

def string_moral_values(text,model='unigram+freq'):
    """Returns the estimated probability that the text is relevant to vices or virtues
       of all moral traits, as a dict.
       The default model is unigram+freq, the best performing (on average) across all
       dataset, according to our work.
       For a list of available models, see get_available_models(). 
       For a list of traits, get_available_prediction_traits().
    """
    
    if model not in models:
        raise ValueError('Invalid model "{}" specified. Valid models are: {}'.format(moral,models))          
    return {moral: estimate(text=text, moral=moral, model=model)[0] for moral in moral_options_predictions}

# def file_moral_value(filename,trait,model):
#   if model not in models:
#       raise ValueError('Invalid model "{}" specified. Valid models are: {}'.format(model,models))      
#   if moral not in moral_options_predictions:
#       raise ValueError('Invalid moral trait "{}" specified. Valid traits are: {}'.format(moral,moral_options_predictions))    
#   
#   return
# 
# def file_moral_values(filename,model):
#   if model not in models:
#       raise ValueError('Invalid model "{}" specified. Valid models are: {}'.format(model,models))      
#   return