<template>
	<main>
		<div class="wrap">
			<div class="text">
				<h1>Здравствуйте, {{ this.full_name }}</h1>
			</div>
		</div>
		
		<div class="wrap">
			<div class="blocks">
				<router-link class="block one" to="/orders">
						<div class="block-text">Мои заказы</div>
				</router-link>

        <router-link to="/catalog" class="block one">
            <div class="block-text">Каталог</div>
        </router-link>

				<router-link to="/create" class="block one">
						<div class="block-text">Оформить заказ</div>
				</router-link>
			</div>
		</div>
		
	</main>
</template>
<script>
export default {
  name: "Autho",
  data() {
    return {
      full_name: document.cookie.replace(/(?:(?:^|.*;\s*)full_name=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      pass: "",
      version: "1.0",
      address: "http://localhost:5000",
      user: {
        full_name: "",
        phone_num: ""
      }
    }
  }
}
</script>

<style scoped>

main{
	display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}

.image{
	width: 35%;
}
img{
	width: 100%;
}

.btn{
	padding: 6px 25px;
}
h1{
	font-size: 3.5em;
	font-weight: bold;
}
.one{

}
.block-text{
  margin-left: 30px;
  margin-bottom: 40px;
	text-align: left;
	font-weight: 500;
	font-size: 2.4em;
	color: white;
}

.block{
	display: flex;
  align-items: flex-end;
  justify-content: left;
  background-color: #184655;
  width: 32.5%;
  border-radius: 15px;
  height: 16rem;
}

.blocks{
	margin-top: 50px;
	width: 100%;
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.wrap{
	width: 80%;
	display: flex;
	justify-content: center;
	align-items: center;
}
.text{
	width: 100%;
  margin-top: 50px;
}

@media (max-width: 1300px){
  h1{
    font-size: 3em;
  }
  .block-text{
    font-size: 2em;
  }
  .block{
    height: 14rem;
    padding-right: 10px;
  }
}

@media (max-width: 950px){
  h1{
    font-size: 2.5em;
  }
  .blocks{
    flex-direction: column;
    margin-top:30px;
  }
  .block{
    width: 100%;
    align-items: center;
    height: 11rem;
    margin-bottom: 15px;
  }
}
@media (max-width: 520px){
  h1{
    font-size: 2em;
  }
}

@media (max-width: 375px){
  h1{
    font-size: 1.9em;
  }
  .text{
    margin-top: 30px;
  }
  .blocks{
    margin-top:20px;
  }
  .block-text{
    font-size: 1.8em;
  }
}
</style>  