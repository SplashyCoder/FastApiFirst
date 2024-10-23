from fastapi import APIRouter,HTTPException

router = APIRouter(prefix='/products', responses={404: {'message': 'No encontrado'}}, tags={'products'})

product_list = ['producto 1','producto 2', 'producto 3']

@router.get('/')
async def productos () :
    return['producto 1','producto 2', 'producto 3']

@router.get('/{id}')
async def productos (id:int) :
    
    return product_list[id]
    
    # try:
    # except:
    #     # raise HTTPException(status_code=404, detail="product id not found")
    #     return{'error':'product not found'}
        
