import enum

from transitions.extensions import GraphMachine as Machine


class ActionEnum(str, enum.Enum):
    """Voting action."""

    ask_for_stocks = 'ask_for_stocks'
    ask_for_steaks = 'ask_for_steaks'
    vote_for_stock = 'vote_for_stock'
    vote_for_steak = 'vote_for_steak'
    finish = 'finish'
    repeat= 'repeat'


class StateEnum(str, enum.Enum):
    """Voting state."""

    initial = 'initial'
    waiting_for_stock = 'waiting_for_stock'
    stock = 'stock'
    nothing_more = 'nothing_more'
    waiting_for_steak = 'waiting_for_steak'
    steak = 'steak'
    finished = 'finished'


transitions = [
    {
        'source': StateEnum.initial, 
        'trigger': ActionEnum.ask_for_stocks,
        'dest': StateEnum.waiting_for_stock,
        'before': 'on_stock_initial',
    },
    # if nothing to buy button is clicked
    {
        'source': StateEnum.waiting_for_stock,
        'trigger': ActionEnum.vote_for_stock,
        'dest': StateEnum.finished,
        'conditions': ['is_nothing_to_buy_cmd'],
    },
    # if nothing more button is clicked
    {
        'source': StateEnum.waiting_for_stock,
        'trigger': ActionEnum.vote_for_stock,
        'dest': StateEnum.nothing_more,
        'conditions': ['is_nothing_more_cmd'],
    },
    # if stock is invalid
    {
        'source': StateEnum.waiting_for_stock,
        'trigger': ActionEnum.vote_for_stock,
        'dest': StateEnum.waiting_for_stock,
        'unless': ['is_stock_valid'],
        'before': ['on_stock_invalid'],
    },
    # stock is good
    {
        'source': StateEnum.waiting_for_stock,
        'trigger': ActionEnum.vote_for_stock,
        'dest': StateEnum.stock,
    },
    # need one more stock
    {
        'source': StateEnum.stock,
        'trigger': ActionEnum.ask_for_stocks,
        'dest': StateEnum.waiting_for_stock,
        'before': ['on_stock_more'],
    },                
    # start voting for steaks
    {
        'source': StateEnum.stock,
        'trigger': ActionEnum.ask_for_steaks,
        'dest': StateEnum.waiting_for_steak,
        'before': ['on_steak_initial'],
    },
    # if voting for steaks is not needed
    {
        'source': StateEnum.stock,
        'trigger': ActionEnum.finish,
        'dest': StateEnum.finished,
        'before': ['on_finish_no_steaks'],
    },
    # specific commands
    {
        'source': StateEnum.nothing_more,
        'trigger': ActionEnum.ask_for_steaks,
        'dest': StateEnum.waiting_for_steak,
        'before': ['on_steak_initial'],
    },
    {
        'source': StateEnum.nothing_more,
        'trigger': ActionEnum.finish,
        'dest': StateEnum.finished,
        'before': ['on_finish_no_steaks'],
    },
    # if voted steak is invalid
    {
        'source': StateEnum.waiting_for_steak,
        'trigger': ActionEnum.vote_for_steak,
        'dest': StateEnum.waiting_for_steak,
        'unless': ['is_steak_valid'],
        'before': ['on_steak_invalid']
    },
    # steak is good
    {
        'source': StateEnum.waiting_for_steak,
        'trigger': ActionEnum.vote_for_steak,
        'dest': StateEnum.steak,
    },
    # finish voting flow
    {
        'source': StateEnum.steak,
        'trigger': ActionEnum.finish,
        'dest': StateEnum.finished,
        'before': ['on_finish'],
    },     
    # repeat
    {
        'source': StateEnum.finished,
        'trigger': ActionEnum.repeat,
        'dest': StateEnum.initial,
    },
]

class Model: pass


machine = Machine(model=Model(), states=StateEnum, transitions=transitions, show_conditions=True)
machine.get_graph().draw('my_state_diagram.png', prog='dot')