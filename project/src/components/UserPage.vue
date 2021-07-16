<template>
	<main>
		<div class="wrap-text">
			<div class="text">
				<h1>Здравствуйте, {{ this.full_name }}</h1>
			</div>
		</div>
		
		<div class="wrap">
			<div class="blocks">
				<router-link class="block one" to="/orders">
					<div class="row">
						<span class="block-text">Мои заказы</span>
					</div>			
				</router-link>

				<router-link to="/create" class="block one">
					<div class="row">
						<span class="block-text">Оформить заказ</span>
					</div>			
				</router-link>

				<router-link to="/plug" class="block one">
					<div class="row">
						<span class="block-text">Программа привилегий</span>
					</div>
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
	width: 100%;
    height: 100%;
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
	font184655-size: 3.5em;
	font-weight: bold;
}
.one{
	background-color: #184655;
	width: 32.5%;
	border-radius: 15px;
	height: 300px;
}
.block-text{
	text-align: left;
	font-weight: 500;
	font-size: 2.4em;
	margin-bottom: 30px;
	margin-left: 30px;
	color: white;
}

.block{
	display: flex;
	align-items: flex-end;
}

.blocks{
	margin-top: 50px;
	width: 80%;
	display: flex;
	justify-content: space-between;
	align-items: center;
}
.wrap-text{
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.wrap{
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}
.text{
	width: 80%;
	padding-top: 60px;
}
	
</style>  