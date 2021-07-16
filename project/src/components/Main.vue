<template>
	<div class="wrap-m">
      <div class="main-m">
        <div class="image">
          <img src="@/assets/store.png">
        </div>
        <div class="main-text">
          <h1 class="main-h1">
            Доставим свежие продукты на дом быстро и просто!
          </h1>
          <button class="btn btn-primary main-btn"><router-link to="/catalog">Попробовать</router-link></button>
      </div>
		</div>
	</div>
</template>

<style scoped>
.main-m{
	width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 90px;
    flex-grow: 1;
}

.image{
	width: 40%;
}
img{
	width: 100%;
}

.main-h1{
	font-size: 3.2em;
	font-weight: bold;
	margin-left: 70px;
}
.main-text{
	width: 40%;
}

.main-btn{
	margin-left: 70px;
	margin-top: 30px;
	font-size: 1.5em;
}
a{
  color: white;
  text-decoration: none;
}

@media (max-width: 1310px){
  .main-h1{
    font-size: 2.5em;
    font-weight: bold;
    margin-left: 70px;
  }
}

@media (max-width: 1040px){
.wrap-m{
  display: flex;
  background-image: url('~@/assets/store.png');
  background-position-y: center;
  background-size: cover;
  color: white;
  flex-grow: 1;
}
  .image{
    display: none;
  }
  .main-m{
    margin-top: 0;
    justify-content: flex-end;
  }
  .main-h1,.main-btn{
    margin-left: 0;
  }
  .main-h1{
    font-size: 2.1em;
  }
  .main-btn{
    font-size: 1.2em;
  }
  .main-text{
    width: 35%;
    background-color: black;
    padding: 20px 30px;
  }
}

@media (max-width: 768px){
  .main-h1{
    font-size: 1.7em;
  }
  .main-btn{
    font-size: 0.8em;
  }
}

@media (max-width: 630px){
  .wrap-m{
    flex-direction: column;
    background-position-y: top;
    background-position-x: center;
  }

  .main-text{
    width: 100%;
    background-color: black;
    padding: 20px 40px;
    position: absolute;
    bottom: 0px;
  }

  .main-h1{
    font-size: 1.3em;
  }

  .main-btn{
    margin-top: 15px;
  }
}

</style>
