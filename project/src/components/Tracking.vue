<template>
  <main>
    <div class="col-md-6 mx-auto text">
      <h1>Отслеживание заказов</h1>
    </div>
    <div class="col-md-6 mx-auto mt-4">
      <form @submit.prevent>
        <h4 class="mb-3">Введите номер заказа</h4>
        <div class="form-group mb-3">
          <input class="form-control" id="number" v-model="number" required>
        </div>
        <div>
          <button class="btn btn-primary btn-lg" @click="findOrder()">Найти</button>
        </div>
      </form>

    </div>

    <div class="found col-md-6 mx-auto" v-if="found">
      <div class="d-flex flex-column mx-auto">
        <h3 class="text-center mr-5">Заказ № {{ order.id }}</h3>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold align-self-left">Статус: </span>{{ order.status }}</p>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold">Заказчик: </span>{{ order.full_name }}</p>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold">Email: </span>{{ order.email }}</p>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold">Телефон: </span>{{ order.phone }}</p>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold">Адрес доставки: </span>{{ order.to }}</p>
        <p style="font-size: 1.3rem;"><span class="font-weight-bold">Стоимость: </span>{{ order.cost }} руб.</p>
      </div>
    </div>

  </main>
</template>

<script>
import Main from "@/components/Main";
export default {
  name: "tracking",
  components: {Main},
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
    }
  }
}

</script>

<style scoped>
.text{
  margin-top: 30px!important;
}
.found{
  margin-top: 40px;
  font-family: 'Open Sans', sans-serif;
  background: #fff;
  padding: 30px 40px;
  border-radius: 12px;
}
h3{
  font-weight: 600;
  font-size: 1.8rem;
}
</style>
