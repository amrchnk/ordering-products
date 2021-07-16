<template>
	<main>
		<div class="wrap">
			<nav aria-label="breadcrumb" class="wrap-in">
				<ol class="breadcrumb">
					<li class="breadcrumb-item base"><router-link to="/userPage">Главная</router-link></li>
					<li class="breadcrumb-item cur">Мои заказы</li>
				</ol>
			</nav>
		</div>

		<div class="wrap text">
			<div class="wrap-in">
				<h1>Мои заказы</h1>
			</div>
		</div>

		<div class="wrap orders">
			<div class="shape wrap-in">
				<div class="order" v-for="(order, index) in orders" :key="order.order_num">
					<h3>Заказ №{{order.order_num}}</h3>
						<table class="table">
							<thead>
                  <th class="dat" scope="col">Дата</th>
                  <th scope="col" class="receiver">Получатель</th>
                  <th scope="col" class="address">Адрес</th>
                  <th scope="col" class="cost">Стоимость (руб.)</th>
                  <th scope="col" class="status">Статус</th>
                  <th scope="col" class="courier">Курьер</th>
							</thead>
							<tbody>
									<td class="dat" scope="row">{{order.order_date}}</td>
									<td class="receiver">{{ order.receiver }}</td>
									<td class="address">{{order.address}}</td>
									<td class="cost">{{order.cost}}</td>
									<td class="status"><b>{{order.last_status}}</b></td>
									<td class="courier">{{order.courier_name}}</td>
							</tbody>
						</table>	
						<div class="order-btns">
							<button class="btn btn-primary" @click="get_order_details(order, index)">Подробности</button>
              <router-link to="/plug"><button class="btn btn-primary" v-if="order.last_status=='Курьер найден'"
                                              @click="sendData(oder.order_num)">Подтвердить передачу заказа</button></router-link>
              <router-link to="/plug"><button class="btn btn-danger">Отменить заказ</button></router-link>
						</div>		
						<div class="items" v-if="index===visible_index">
							<div class="map" id="map" v-if="map_ready===true">
                <yandex-map
                    :coords="[order.courier_coords.location_1, order.courier_coords.location_2]"
                    :zoom="10"
                >
                  <ymap-marker
                      :coords="[order.courier_coords.location_1, order.courier_coords.location_2]"
                      marker-id="124"
                      hint-content="some hint"
                  />
                </yandex-map>
							</div>
              <div class="map" v-if="order.details.courier_id===0">
                <h3>Ищем курьера</h3>
              </div>
							<div class="details">
                <h3 class="orders-h3">Дата заказа: {{order.details.order_date}}</h3>
                <h3 class="orders-h3">Отправитель: {{order.details.full_name_from}} {{order.details.phone_from}}</h3>
                <h3 class="orders-h3">Пункт отправления: {{order.details.adr_from}}</h3>
                <h3 class="orders-h3">Получатель: {{order.details.full_name_to}} {{order.details.phone_to}}</h3>
								<h3 class="orders-h3">Пункт назначения: {{order.details.adr_to}}</h3>
							</div>
						</div>
				</div>
			</div>


		</div>
		
	</main>
</template>

<script>

export default {
  name: "Orders",
  data() {
    return {
      coords: [0,0],
      map_ready: false,
      orders: [{
        details_visible: false,
        courier_coords: {
          location_1: 0,
          location_2: 0
        },
        details:{
          courier_id: 0,
        }
      }],
      detailed_order: {},
      pass: document.cookie.replace(/(?:(?:^|.*;\s*)pass=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      address: "http://localhost:5000",
      visible_index: -1
    }
  },
  components: {},
  methods: {
    async get_order_details(order, index){
      order.details_visible=!order.details_visible;
      this.map_ready = false;
      await this.$http.get(`${this.address}/get_order_details_client/${this.email}/${this.pass}/${order.order_num}`)
          .then((res) => res.json()).then((res) => (order.details = res[0]));
      this.visible_index = index;
      if (order.details.courier_id !== 0)
        await this.get_courier_coords(order, order.details.courier_id);
    },
    async get_courier_coords(order, courier_id){
      let coords = {location_1: 0, location_2: 0};
      await this.$http.get(`${this.address}/get_courier_coords/${this.email}/${this.pass}/${courier_id}`)
          .then((res) => res.json()).then((res) => (coords = res[0]));
      order.courier_coords.location_1 = coords.location_1;
      order.courier_coords.location_2 = coords.location_2;
      console.log(order.courier_coords);
      this.map_ready = true;

    },
    async sendData(order_number){
      let result;
      await this.$http.get(`${this.address}/send_email/${this.email}/${this.pass}/${order_number}`)
          .then((res) => res.text()).then((res) => (result = res));
    },
    async get_orders() {
      if (this.email.length > 0 && this.pass.length > 0) {// Проверяем, чтобы поля логина и пароля не были пустыми
        try {
          await this.$http.get(`${this.address}/get_orders/${this.email}/${this.pass}`)
              .then((res) => res.json()).then((res) => (this.orders = res));
          if (this.orders === -1 || this.orders === null) { // Если вход успешен, записываем пользователя в cookie
            alert("Произошла ошибка, повторите вход");
          } else if (this.orders === 0){
            alert("У вас нет заказов");
          }
          for (let order of this.orders){
            order.details_visible = false;
            order.courier_coords = {location_1: 0, location_2: 0};
          }
        } catch (e) {
          console.log(e);
          alert("Сервер недоступен, попробуйте позже");
        }
      } else
        alert("Поля email и password не могут быть пустыми");
    }
  },
  async created() {
    // При открытии смотрим куки. При наличии логина и пароля - пытаемся авторизоваться
    let email = document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1");
    let password = document.cookie.replace(/(?:(?:^|.*;\s*)pass=\s*([^;]*).*$)|^.*$/, "$1");
    if (email === "" || password === "")
      await this.$router.push('/userPage');
    await this.get_orders();
  }
}
</script>

<style scoped>
ol{
	font-size: 1.2em;
	color: #5B5B5E;
}

a{
	color: #5B5B5E;
}

.cur{
	font-weight: 600;
}

main{
	width: 100%;
    height: 100%;
}

.orders-h3{
	text-align:left;
	font-weight:400;
	margin-left: 30px;
	margin-top:20px;
}

.wrap{
	width: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}

.wrap-in{
	width: 80%;
}

.shape{
	
}
.order{
	background-color: white;
	padding:30px 30px !important;
	border-radius: 10px;
	margin-bottom: 20px;
}

nav{
	margin-top: 50px;
}
h1{
	font-size: 3em;
	font-weight: bold;
	text-align: left;
}

a{
	text-decoration: none !important;
}

.dat{
	width: 	15%;
}

.receiver{
	width: 	15%;
}

.cost{
	width: 	15%;
}

.status{
	width: 	15%;
}

b{
	padding: 0;
}

td.status{
	color: orange;
}

.address{
	width: 	25%;
}

.courier{
	width: 	20%;
}

table{
	margin-top: 20px;
}

.orders{
	font-family: 'Open Sans', sans-serif;
	margin-top: 20px;
}

h3{
  font-size: 1em;
	font-weight: 600;
}

.order-btns{
	display: flex;
}
button router-link{
	text-align: center !important;
	width: 100px;
	margin-top: 20px;
}

.items{
	width: 100%;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
}

.map{
	width:30%;
	height:300px;
}
</style>