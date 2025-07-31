from fastapi import APIRouter,status,HTTPException, Depends
from sqlmodel import Session,select
from .. import schemas,database,model,oauth2

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.vote,session:Session = Depends(database.get_session),current_user:dict = Depends(oauth2.get_current_user)):
    
    post_query = select(model.Post).where(model.Post.id == vote.post_id)
    post_result = session.exec(post_query).first()
    print(post_result)
    if not post_result :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {vote.post_id} does not exist")
    
    statement = (
        select(model.vote)                                   # ← SQLModel’s select
        .where(
            model.vote.post_id == vote.post_id,                   # correct column/value
            model.vote.user_id == current_user.id            # second condition # type: ignore
        )
    )
        
    existing_vote = session.exec(statement).first()
    if (vote.dir == True): #this for liking a post
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}") # type: ignore
        new_vote = model.vote(post_id=vote.post_id, user_id=current_user.id) # type: ignore
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added"}
    # Remove a like
    else:
        if not existing_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vote does not exist"
            )
        session.delete(existing_vote)
        session.commit()
        return {"message": "Vote removed"}