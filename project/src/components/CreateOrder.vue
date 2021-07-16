<template>
	<main>
		<Modal v-if="visible" @closeModal="closeModal" ref="Modal"/>
		<div class="wrap">
			<nav aria-label="breadcrumb" class="wrap-in nav-in">
				<ol class="breadcrumb">
					<li class="breadcrumb-item"><router-link to="/userPage">Главная</router-link></li>
					<li class="breadcrumb-item cur">Оформить заказ</li>
				</ol>
			</nav>
		</div>

		<div class="wrap">
			<div class="wrap-in">
				<h1>Оформить заказ</h1>
			</div>
		</div>

		<div class="wrap">
			<div class="wrap-in steps">
				<div class="first margin">
					<div class="text">
						<h3>1. Для оформления заказа укажите следующие данные:</h3>
					</div>

					<div class="form">
							<div class="sender part">
								<h4>Отправитель</h4>
								<hr>
								<div class="str">
									<div class="field">
										<label class="form-label">Имя отправителя</label>
										<input class="form-control" v-model="sender.name">
									</div>

									<div class="field">
										<label class="form-label">Телефон</label>
										<input class="form-control" v-model="sender.phone">
									</div>
								</div>

								<div class="str">
									<div class="field">
										<label class="form-label">Адрес</label>
                    <yandex-map
                        :coords="coords"
                        :zoom="10"
                        @click="onClick_S"
                    >
                      <ymap-marker
                          :coords="coords"
                          marker-id="123"
                          hint-content="some hint"
                      />
                    </yandex-map>
									</div>
								</div>
                <div class="str">
                  <div class="field">
                    <label class="form-label">Комментарий к заказу</label>
                    <textarea class="form-control" v-model="sender.comment"></textarea>
                  </div>
                </div>
							</div>

							<div class="receiver part">
								<h4>Получатель</h4>
								<hr>

								<div class="str">
									<div class="field">
										<label class="form-label">Имя получателя</label>
										<input class="form-control" v-model="receiver.name">
									</div>

									<div class="field">
										<label class="form-label">Телефон</label>
										<input class="form-control" v-model="receiver.phone">
									</div>
								</div>

								<div class="str">
									<div class="field">
										<label class="form-label">Адрес</label>
                    <yandex-map
                        :coords="coords"
                        :zoom="10"
                        @click="onClick_R"
                    >
                      <ymap-marker
                          :coords="coords"
                          marker-id="124"
                          hint-content="some hint"
                      />
                    </yandex-map>
									</div>
								</div>
                <div class="str">
                  <div class="field">
                    <label class="form-label">Комментарий к заказу</label>
                    <textarea class="form-control" v-model="receiver.comment"></textarea>
                  </div>
                </div>
							</div>

							<div class="cost part">
								<h2>К оплате: {{price_rub}}</h2>
							</div>
					</div>
				</div>

				<div class="second margin">
					<div class="text">
						<h3>2. Выберите способ оплаты</h3>
						<div class="form-check part">
							<input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
							<label class="form-check-label" for="flexRadioDefault1">
								Оплата курьеру при отправке
							</label>
						</div>

						<div class="form-check margin-check">
							<input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
							<label class="form-check-label" for="flexRadioDefault2">
								Оплата картой онлайн
							</label>
						</div>

						<div class="card" v-if="false">
							<div class="str-date">
									<div class="field number">
										<label class="form-label">Номер карты</label>
										<input class="form-control" placeholder="XXXX-XXXX-XXXX-XXXX">
									</div>

									<div class="field owner">
										<label class="form-label">Держатель карты</label>
										<input class="form-control" placeholder="IVAN IVANOV">
									</div>
							</div>

							<div class="str-date margin-card">
									<div class="field date">
										<label class="form-label">Срок действия</label>
										<input class="form-control" placeholder="ММ/ГГ">
									</div>

									<div class="field CVC">
										<label class="form-label">CVC-код</label>
										<input class="form-control" placeholder="XXX">
									</div>

									<div class="logo owner">
										<img src="@/assets/logo.svg">
									</div>
							</div>
						</div>
						<button class="btn btn-warning pay" @click="ShowModal">
							Оплатить
						</button>
					</div>
				</div>

				<div class="third margin">

				</div>

			</div>
		</div>
	</main>
</template>

<!--<script>-->
<!--	export default {-->
<!--		name: 'App',-->
<!--		components:{-->
<!--			Modal-->
<!--		},-->
<!--		data(){-->
<!--			return{-->
<!--				visible:false,-->
<!--        email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1"),-->
<!--        pass: document.cookie.replace(/(?:(?:^|.*;\s*)pass=\s*([^;]*).*$)|^.*$/, "$1"),-->
<!--        coords:[55.753220, 37.622513],-->
<!--        order_num: 0,-->
<!--        order: {},-->
<!--        address: "http://localhost:5000",-->
<!--        client: {-->
<!--					id: document.cookie.replace(/(?:(?:^|.*;\s*)id=\s*\s*([^;]*).*$)|^.*$/, "$1"),-->
<!--					surname: document.cookie.replace(/(?:(?:^|.*;\s*)full_name=\s*\s*([^;]*).*$)|^.*$/, "$1").split(' ')[0],-->
<!--				  name: "",-->
<!--					patronymic: "",-->
<!--					email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1"),-->
<!--          phone: "",-->
<!--        },-->
<!--        price:0,-->
<!--        price_rub: ""-->
<!--			}-->
<!--		},-->
<!--    mounted() {-->
<!--      this.price-->
<!--    },-->
<!--		methods:{-->
<!--      getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {-->
<!--        var R = 6371; // Radius of the earth in km-->
<!--        var dLat = this.deg2rad(lat2-lat1);  // deg2rad below-->
<!--        var dLon = this.deg2rad(lon2-lon1);-->
<!--        var a =-->
<!--            Math.sin(dLat/2) * Math.sin(dLat/2) +-->
<!--            Math.cos(this.deg2rad(lat1)) * Math.cos(this.deg2rad(lat2)) *-->
<!--            Math.sin(dLon/2) * Math.sin(dLon/2)-->
<!--        ;-->
<!--        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));-->
<!--        var d = R * c; // Distance in km-->
<!--        return d;-->
<!--      },-->

<!--      deg2rad(deg) {-->
<!--        return deg * (Math.PI/180)-->
<!--      },-->
<!--      onClick_S(e) {-->
<!--        this.coords = e.get('coords');-->
<!--        this.sender.coord1=this.coords[0];-->
<!--        this.sender.coord2=this.coords[1];-->
<!--        if(this.receiver.coord1!==0){-->
<!--          this.price=100*this.getDistanceFromLatLonInKm(this.sender.coord1,this.sender.coord2,this.receiver.coord1,this.receiver.coord2)-->
<!--        }-->
<!--      },-->
<!--      onClick_R(e) {-->
<!--        this.coords = e.get('coords');-->
<!--        this.receiver.coord1=this.coords[0];-->
<!--        this.receiver.coord2=this.coords[1];-->
<!--        if(this.sender.coord1!==0){-->
<!--          this.price=Math.round(100*this.getDistanceFromLatLonInKm(this.sender.coord1,this.sender.coord2,this.receiver.coord1,this.receiver.coord2));-->
<!--          this.price_rub = this.price +' руб.';-->
<!--        }-->
<!--      },-->
<!--      async ShowModal(){-->
<!--        await this.$http.post(`${this.address}/post_order/${this.email}/${this.pass}`, {sender: this.sender, receiver: this.receiver, cost: this.price})-->
<!--            .then((res) => this.order_num = res.data);-->
<!--        document.cookie = `order_num=${this.order_num}`;-->
<!--        console.log(this.order_num);-->

<!--        await this.$http.get(`${this.address}/get_order_details_client/${this.email}/${this.pass}/${this.order_num}`)-->
<!--            .then((res) => res.json()).then((res) => (this.order = res));-->
<!--        console.log(this.order);-->
<!--        document.cookie = `order=${this.order[0]}`;-->
<!--        alert("Заказ создан");-->
<!--        await this.$router.push({path: `/userPage/`});-->
<!--        //this.visible=true-->

<!--			},-->
<!--			closeModal(){-->
<!--				this.visible=false-->
<!--			}-->
<!--		}-->
<!--	}-->
<!--</script>-->


<style>
h3{
	font-size: 1.5em;
}

.ymap-container {
  height: 300px;
  width: 800px;
}

.date{
	width: 30% !important;
}

.owner{
	margin-left: 20px;
}

.logo{
	width: 50%;
	display: flex;
	align-items: flex-end;
}

img{
	width: 100%;
}

.margin-card{
	margin-top: 50px;
}

.CVC{
	width: 20% !important;
	margin-left: 20px;
}

.nav-in{
	margin-top:50px;
}

h4{
	font-size: 1.2em;
	font-weight: 600;
}

.pay{
	margin-top:15px;
	width: 150px;
}

.str-date{
	width: 100%;
	display: flex;
}

.card{
	margin-top: 20px;
	width: 50%;
	padding: 40px 30px;
	border-radius: 15px;

}

h2{
	font-weight: bold;
	font-size: 2em;
}

.margin-check{
	margin-top: 15px;
}

main{
	width: 100%;
    height: 100%;
}

.wrap{
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.label-radio{
	margin-left: 15px;
}
.part{
	margin-top: 30px;
	width: 100%;
}

.field{
	width:48%;
    text-align:left;

}

.str{
	width: 100%;
	margin-top: 20px;
	display: flex;
	justify-content: space-between;
}

hr{
	margin:10px 0;
}

.wrap-in{
	width: 80%;;
}

.steps{
	background-color: white;
	margin-top: 15px;
	border-radius: 15px;
	font-family: 'Open Sans', sans-serif;
}
h1{
	font-size: 3em;
	font-weight: bold;
	text-align: left;
}

a{
	text-decoration: none !important;
	color: #5B5B5E;
}

ol{
	font-size: 1.2em;
	color: #5B5B5E;
}

.cur{
	font-weight: 600;
}

.margin{
	margin: 50px;
}


</style>
