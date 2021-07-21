<template>
  <main>
    <div class="wrap">
      <div class="text">
        <h1>Отслеживание заказов</h1>
      </div>
    </div>

    <div class="wrap">
      <div class="container">
        <div class="col_one_wrap">
          <div class="col_one">
            <h4>Введите номер заказа:</h4>
            <input class="form-control" id="number" v-model="number" required>
            <button class="btn btn-primary" @click="findOrder()">Найти</button>
          </div>
        </div>

        <div class="col_two_wrap">
          <div class="col_two">
            <h3>Детали заказа</h3>
            <div class="not_found" v-if="!found">
              <div class="image">
                <img src="@/assets/searcher.svg" alt="">
              </div>
              <div class="image_text">
                <h2>Упс! <br>Пока что ничего не найдено</h2>
              </div>
            </div>
            <div class="found" v-if="found">
              <div>
                <h3 class="order_title">Заказ № {{ order.id }}</h3>
                <p class="order_rows"><span>Статус: </span>{{ order.status }}</p>
                <p class="order_rows"><span>Заказчик: </span>{{ order.full_name }}</p>
                <p class="order_rows"><span>Email: </span>{{ order.email }}</p>
                <p class="order_rows"><span>Телефон: </span>{{ order.phone }}</p>
                <p class="order_rows"><span>Стоимость: </span>{{ order.cost }} руб.</p>
                <p class="order_rows"><span>Адрес доставки: </span>{{ order.to }} <a class="order_link" href="#" @click="ShowMap"> Показать на карте</a></p>
<!--                <div class="order_rows">-->
<!--                  <yandex-map-->
<!--                      :coords="coords"-->
<!--                      :zoom="10"-->
<!--                      @click="onClick"-->
<!--                  >-->
<!--                    <ymap-marker-->
<!--                        :coords="coords"-->
<!--                        marker-id="124"-->
<!--                        hint-content="some hint"-->
<!--                    />-->
<!--                  </yandex-map>-->
<!--                </div>-->

              </div>
            </div>
          </div>
        </div>
      </div>

    </div>



  </main>
</template>

<script>
import Main from "@/components/Main";
import { yandexMap, ymapMarker } from 'vue-yandex-maps';
import PayError from "@/components/PaymentOrderError";

export default {
  name: "tracking",
  components: {Main,
  yandexMap,
  ymapMarker
  },
  data() {
    return {
      number: "",
      order: {
        id: "",
        status: "",
        full_name: "",
        email: "",
        phone: "",
        to: "",
        cost: 0
      },
      coords:[,],
      found: false,
      address_orders: "http://localhost:5001", //drop later
      address: "http://localhost:5000"
    }
  },
  methods: {
    async findOrder() {
      try {
        let request = {
          "jsonrpc": "2.0",
          "method": "App.get_order",
          "params": {
            "id_order": Number.parseInt(this.number)
          },
          "id": 1
        }
        let response = {};
        await this.$http.post(`${this.address_orders}/orders`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response.error === "Order not found") {
          this.found = false;
          alert("Заказ с таким номером не найден");
        }
        else {
          this.found = true;
          this.order.id = response.id;
          this.order.status = response.status;
          this.order.to = response.address;
          this.order.cost = response.cost;
          await this.getClient(response.id_client);
        }
      }
      catch (err) {
        console.log(err);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async getClient(id_client) {
      try {
        let request = {
          "jsonrpc": "2.0",
          "method": "App.get_user",
          "params": {
            "id_user": id_client
          },
          "id": 1
        }
        let response = {};
        await this.$http.post(`${this.address}/clients`, request)
          .then((res) => res.json()).then((res) => (response = res.result));
        if (response.error === "User not found") {
          alert("Пользователь не найден");
          this.order.full_name = "Не найдено";
          this.order.email = "Не найдено";
          this.order.phone = "Не найдено";
        }
        else {
          this.order.full_name = response.full_name;
          this.order.email = response.email;
          this.order.phone = response.phone;
        }
      }
      catch (e) {
        console.log(e);
        alert("Сервер недоступен, попробуйте позже");
      }
    },
    async ShowMap(){
      // try{
        await ymaps.geocode(this.order.to).then((res) => (res.geoObjects));
        console.log(res)
      // }
      //   // await ymaps.geocode(this.order.to).then((res) => (this.coords = res.geoObjects.get(0).properties.get('text')));      }
      // catch (e) {
      //   console.log(e);
      //   alert(e);
      // }
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

.wrap{
  width: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.text{
  width: 100%;
  margin-top: 50px;
}

h1{
  font-size: 3.4em;
  font-weight: bold;
}

.col_one_wrap{
  width: 30%;
}

.col_two_wrap{
  width: 70%;
}
.col_one,.col_two{
  background-color: white;
  border-radius: 10px;
}
.col_one{
  margin-right: 15px;
  padding: 25px;
}

.col_two{
 display: flex;
  flex-direction: column;
  padding: 30px;
}
.container{
  padding: 0;
  margin: 20px 0;
  display: flex;
  width: 100%;
}

h4{
  font-size: 1.2em;
  font-weight: 400;
}

input,button{
margin-top: 15px;
}

h3 {
  font-weight: 400;
  font-size: 1.6em;
}

.not_found{
  display: flex;
  justify-content: center;
}
.image{
  padding: 20px;
  width: 40%;
}
.image_text{
  padding: 0 40px;
  width: 60%;
  display: flex;
  align-items: center;
  color: darkslateblue;
  font-size: 1.2em;
}
img{
  width: 100%;
}
.order_title{
  font-weight: bold;
}
.found{
  margin-top: 20px;
  font-family: 'Open Sans', sans-serif;
}
.order_rows{
  margin: 0;
  font-size: 1.2em;
  margin-bottom: 8px;
}

.order_link{
  color: #2787F5;
  font-size: 0.8em;
}

@media (max-width: 1350px){
  h1{
    font-size: 3em;
  }
  h2{
    font-size: 1.8em;
  }
  .image_text{
     padding: 0 30px;
   }
}

@media (max-width: 1280px){
h4{
  font-size: 1em;
}
  h2{
    font-size: 1.6em;
  }
h3{
  font-size: 1.3em;
}
input,button{
  font-size: 0.8em;
}
  .image_text{
    padding: 0 20px;
  }
}

@media (max-width: 1080px){
  h1{
    font-size: 2.5em;
  }
  h2{
    font-size: 1.4em;
  }
  input,button{
    font-size: 0.7em;
  }
  .image_text{
    padding-right: 0;
  }
}

@media (max-width: 980px) {
.container{
  flex-direction: column;
}
  .col_one_wrap,.col_two_wrap{
    width: 100%;
  }
  .col_one_wrap{
    margin-bottom: 15px;
  }
  .col_one{
    margin-right: 0;
  }
  h4{
    font-size: 1em;
  }
  h2{
    font-size: 1.6em;
  }
  h3{
    font-size: 1.3em;
  }
  input,button{
    font-size: 0.8em;
  }
  .image_text{
    padding: 0 20px;
  }
}

@media (max-width: 768px) {
  h2{
    font-size: 1.3em;
  }
  .image_text{
    padding: 0 10px;
  }
  h3{
    font-size: 1.1em;
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: 2.3em;
  }
  .not_found{
    flex-direction: column;
  }

}

@media (max-width: 380px) {
  h1 {
    font-size: 2em;
  }

}
</style>
