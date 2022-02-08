from typing import Optional

from fastapi import APIRouter, Request, Response, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from app.templates import templates
from app.models import VoteQuestion, Vote, VoteAnswer
from app.db import db_session 
from app.modules import auth

router = APIRouter(prefix='/votes', tags=['surveys'])


@router.get('/get/{id}', response_class=HTMLResponse)
def get_survey(id:int, request:Request):
    user = auth.get_user_session(request)
    resp = Vote.get_vote(id)
    '''Отвечал ли пользователь на этот вопрос. Аноним == None'''
    answered: VoteAnswer = db_session.query(VoteAnswer).filter(VoteAnswer.vote_id == resp.id and VoteAnswer.user_id == user.id).first() if user else None
    print('Answered:',answered)
    def is_allowed(answered, anon, revote, closed):
        if closed:
            return {'allowed': False, 'reason': 'Голосование закрыто!'}
        if not anon and not user:
            return {'allowed': False, 'reason': 'Анонимно голосовать нельзя!'}
        if not revote and answered:
            return {'allowed': False, 'reason': 'Повторно голосовать нельзя!'}
        else:
            return {'allowed': True, 'reason': 'Открытое голосование'}
        
    vote_allowed = is_allowed(answered, resp.anon, resp.revote, resp.closed)
    print(vote_allowed)
    return templates.TemplateResponse('vote.html', {'request': request, 'data': resp, 'title': resp.title, 'user' : user, 'allowed': vote_allowed})

@router.get('/add', response_class=HTMLResponse)
def vote_creation(request: Request):
    user = auth.get_user_session(request)
    if user:   
        return templates.TemplateResponse('create-vote.html', {'request': request, 'title':'Создание голосования', 'user': user})
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER, )


@router.post('/vote/{vote_id}')
def vote_for(vote_id: int, request: Request, answer: int = Form(...), question_id: int = Form(...)):
    '''Отправка ответа на в БД для голосования с id == vote_id'''
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    user_id = None if not user else user.id
    print(f'user_id: {user_id} vote_anon: {vote.anon}')
    if not user_id and not vote.anon:
        return {'Anon voting' : 'Not allowed!'}
    new_answer = VoteAnswer(user_id, vote_id, question_id, answer)
    db_session.add(new_answer)
    db_session.commit()
    return RedirectResponse(f'/votes/get/{vote_id}', status_code=status.HTTP_303_SEE_OTHER)

@router.post('/add')
def add_vote(
    request: Request, 
    title: str = Form(...), 
    answers: str = Form(...), 
    description: str = Form(...), 
    question: str = Form(...),
    anon: Optional[bool] = Form(default=False),
    revote: Optional[bool] = Form(default=False)   
            ):
    
    print(anon, revote)
    user = auth.get_user_session(request)
    if user:
        print(title, answers, description, anon, revote)
        answers = answers.split(',')
        new_vote = Vote(title, user.id, description, anon, revote)
        db_session.add(new_vote)
        db_session.commit()
        new_question = VoteQuestion(new_vote.id, question, answers)
        db_session.add(new_question)
        db_session.commit()
        RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/edit/{vote_id}')
def edit_view(vote_id: int, request:Request):
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    if not user:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)
    if not vote:
        response = Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
        return response
    if user.id == vote.creator_id:
        return {'body': 'You can edit this!'}
    else:
        return {'body': 'You cant edit this!'}