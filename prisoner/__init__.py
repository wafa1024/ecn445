
from otree.api import *
c = cu

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class C(BaseConstants):
    NAME_IN_URL = 'prisoner'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    PAYOFF_A = cu(300)
    PAYOFF_B = cu(200)
    PAYOFF_C = cu(100)
    PAYOFF_D = cu(0)
    INSTRUCTIONS_TEMPLATE = 'prisoner/instructions.html'
class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass
def set_payoffs(group: Group):
    for p in group.get_players():
        set_payoff(p)
class Player(BasePlayer):
    cooperate = models.BooleanField(choices=[[True, 'Cooperate'], [False, 'Defect']], doc='This player s decision', widget=widgets.RadioSelect)
def other_player(player: Player):
    group = player.group
    return player.get_others_in_group()[0]
def set_payoff(player: Player):
    payoff_matrix = {
        (False, True): C.PAYOFF_A,
        (True, True): C.PAYOFF_B,
        (False, False): C.PAYOFF_C,
        (True, False): C.PAYOFF_D,
    }
    other = other_player(player)
    player.payoff = payoff_matrix[(player.cooperate, other.cooperate)]
class Introduction(Page):
    form_model = 'player'
    timeout_seconds = 100
class Decision(Page):
    form_model = 'player'
    form_fields = ['cooperate']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player: Player):
        opponent = other_player(player)
        return dict(
            opponent=opponent,
            same_choice=player.cooperate == opponent.cooperate,
            my_decision=player.field_display('cooperate'),
            opponent_decision=opponent.field_display('cooperate'),
        )
page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
