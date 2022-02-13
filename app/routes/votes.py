from ast import For
from typing import Optional
from urllib import response

from fastapi import APIRouter, Request, Response, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import and_

from app.templates import templates
from app.models import VoteQuestion, Vote, VoteAnswer
from app.db import db_session 
from app.modules import auth

def is_allowed(user,answered: VoteAnswer, anon:Vote.anon, revote:Vote.revote, closed: Vote.closed) -> dict:
        if closed: #закрытое голосование
            return {'allowed': False, 'reason': 'Голосование закрыто!'}
        if not anon and not user: #неанонимное голосование
            return {'allowed': False, 'reason': 'Анонимно голосовать нельзя!'}
        if not revote and answered:
            return {'allowed': False, 'reason': 'Повторное голосование запрещено!'}
        else:
            return {'allowed': True, 'reason': 'Голосование доступно!'}


router = APIRouter(prefix='/votes', tags=['surveys'])


@router.get('/get/{id}', response_class=HTMLResponse)
def get_vote(id:int, request:Request):
    user = auth.get_user_session(request)
    resp = Vote.get_vote(id)
    if not resp:
        return Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    '''Отвечал ли пользователь на этот вопрос. Аноним == None'''
    answered: VoteAnswer = db_session.query(VoteAnswer).filter(and_(VoteAnswer.vote_id == resp.id, VoteAnswer.user_id == user.id)).first() if user else False
    vote_allowed = is_allowed(user, answered, resp.anon, resp.revote, resp.closed)
    author = True if user and  user.id == resp.creator_id else False
    return templates.TemplateResponse('vote.html', {'request': request, 'data': resp, 'title': resp.title, 'user' : user, 'allowed': vote_allowed, 'author' : author})

@router.get('/add', response_class=HTMLResponse)
def vote_creation(request: Request):
    user = auth.get_user_session(request)
    if user:   
        return templates.TemplateResponse('create-vote.html', {'request': request, 'title':'Создание голосования', 'user': user})
    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER, )


@router.post('/vote/{vote_id}')
def vote_for(vote_id: int, request: Request, answer: Optional[int] = Form(default=None), question_id: int = Form(...)):
    '''Отправка ответа на голосование в БД для голосования с id == vote_id'''
    if answer is None:
        return 'Пустой ответ не принимается.'
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    if not vote:
        return Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    if vote.closed:
        return 'Not allowed, vote closed!'
    user_id = None if not user else user.id
    if not user_id and not vote.anon:
        return {'Anon voting' : 'Not allowed!'}
    new_answer = VoteAnswer(user_id, vote_id, question_id, answer)
    db_session.add(new_answer)
    db_session.commit()
    return RedirectResponse(f'/votes/result/{vote_id}', status_code=status.HTTP_303_SEE_OTHER)

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
    '''Создание голосования'''
    print(anon, revote)
    user = auth.get_user_session(request)
    if user:
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
def edit_vote_view(vote_id: int, request:Request):
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    if not user:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)
    if not vote:
        return Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    if user.id == vote.creator_id:
        answers = ','.join(vote.questions[0].answers)
        return templates.TemplateResponse('edit-vote.html', {'request': request, 'vote' : vote, 'answers' : answers, 'user' : user, 'title': 'Редактирование опроса'  })
    else:
        return {'body': 'You cant edit this!'}

@router.post('/edit/{vote_id}')
def edit_vote_update(vote_id: int, request: Request, 
        title: str = Form(...), 
        description: str = Form(...), 
        anon: bool = Form(default=False), 
        revote: bool = Form(default=False), 
        question: str = Form(default=None),
        answers: str = Form(default=None),
        visible: bool = Form(default=False),
        closed: bool = Form(default=False)
        ):
    '''Редактирование голосования'''
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    if not vote:
        Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    if not user or user.id != vote.creator_id:
        return {'Edit' : 'Not allowed'}
    print(visible)
    vote.update(title, description, bool(anon), bool(revote), closed, visible)
    if question and answers:
        answers = answers.split(',')
        vote.questions[0].update(question, answers)
    return RedirectResponse(f'/votes/get/{vote.id}', status_code=status.HTTP_303_SEE_OTHER)
    
@router.post('/delete/{vote_id}')
def delete(vote_id: int, request:Request):
    user = auth.get_user_session(request)
    vote = Vote.get_vote(vote_id)
    if not vote:
        Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    if user and user.id == vote.creator_id:
        vote.delete()
    return {'Vote_id': vote.id,
            'Operation': 'Deleted'}

@router.get('/result/{vote_id}')
def result(vote_id: int, request: Request):
    user = auth.get_user_session(request)
    if not user:
        return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)
    vote = Vote.get_vote(vote_id)
    if not vote:
        Response('Not found', status_code=status.HTTP_404_NOT_FOUND)
    results = vote.get_results() 
    return templates.TemplateResponse('result.html', {'request': request, 'results': results, 'title': 'Результаты опроса', 'user': user, 'vote':vote}) 
