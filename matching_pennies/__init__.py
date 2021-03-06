
from otree.api import *
c = cu

doc = "\nA demo of how rounds work in oTree, in the context of 'matching pennies'\n"
class C(BaseConstants):
    NAME_IN_URL = 'matching_pennies'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    STAKES = cu(100)
    MATCHER_ROLE = 'Matcher'
    MISMATCHER_ROLE = 'Mismatcher'
class Subsession(BaseSubsession):
    pass
def creating_session(subsession: Subsession):
    session = subsession.session
    import random
    
    if subsession.round_number == 1:
        paying_round = random.randint(1, C.NUM_ROUNDS)
        session.vars['paying_round'] = paying_round
    if subsession.round_number == 3:
        # reverse the roles
        matrix = subsession.get_group_matrix()
        for row in matrix:
            row.reverse()
        subsession.set_group_matrix(matrix)
    if subsession.round_number > 3:
        subsession.group_like_round(3)
class Group(BaseGroup):
    pass
def set_payoffs(group: Group):
    session = group.session
    subsession = group.subsession
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    for p in [p1, p2]:
        is_matcher = p.role == C.MATCHER_ROLE
        p.is_winner = (p1.penny_side == p2.penny_side) == is_matcher
        if subsession.round_number == session.vars['paying_round'] and p.is_winner:
            p.payoff = C.STAKES
        else:
            p.payoff = cu(0)
class Player(BasePlayer):
    penny_side = models.StringField(choices=[['Heads', 'Heads'], ['Tails', 'Tails']], label='I choose', widget=widgets.RadioSelect)
    is_winner = models.BooleanField()
class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']
    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs
class ResultsSummary(Page):
    form_model = 'player'
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS
    @staticmethod
    def vars_for_template(player: Player):
        session = player.session
        player_in_all_rounds = player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )
page_sequence = [Choice, ResultsWaitPage, ResultsSummary]
