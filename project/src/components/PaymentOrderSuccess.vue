<template>
	<main class="modal-main">
		<div class="modal-wrap">
			<div class="modal-header">
				<h2 class="modal-h2">Заказ №{{ this.order_num}} оформлен</h2>
				<span ><i class="material-icons" @click="closeModal">close</i></span>
			</div>
			<div class="modal-body">
				<h3 class="modal-h3">Детали заказа</h3>
				<table class="modal-table">
					<tbody>
						<tr>
							<td class="left">
								Дата:
							</td>
							<td class="right">
								{{this.order.order_date}}}
							</td>
						</tr>

						<tr>
							<td class="left">
								Заказчик:
							</td>
							<td class="right">
								{{this.order.full_name_from}}}\n{{this.order.str_adr_from}}}
							</td>
						</tr>

						<tr>
							<td class="left">
								Цена заказа:
							</td>
							<td class="right">
								{{ this.order.cost }} руб.
							</td>
						</tr>
					</tbody>
				</table>
				<hr>
				<div class="modal-table">
						<tr>
							<td class="left">
								Заказ прибудет к:
							</td>
							<td class="right">
								{ДатаВремя} (оставшееся время)
							</td>
						</tr>
				</div>
			</div>

		</div>
	</main>

</template>
<script>
export default {
  name: 'Modal',
  data(){
    return {
      order_num: document.cookie.replace(/(?:(?:^|.*;\s*)order_num=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      order: document.cookie.replace(/(?:(?:^|.*;\s*)order=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      address: "http://tpis.std-913.ist.mospolytech.ru",
      pass: document.cookie.replace(/(?:(?:^|.*;\s*)pass=\s*\s*([^;]*).*$)|^.*$/, "$1"),
      email: document.cookie.replace(/(?:(?:^|.*;\s*)email=\s*\s*([^;]*).*$)|^.*$/, "$1")
    }
  },
  methods:{
    async created(){

    },
    async get_order_details(){

    },
    closeModal(){
      this.$emit('closeModal')
    }

  }
}

</script>
<style scoped>
	.modal-main{
		display: flex;
		height: 100%;
		justify-content: center;
		position: absolute;
		top: 0;
		bottom: 0;
		left: 0;
		right: 0;
		background-color: rgba(50,50,50,0.4);
	}
	.modal-h2{
		color: #417158;
		font-size: 1.5em;
		font-weight: 600;
		margin-bottom: 10px;
	}

	.modal-h3{
		font-weight: bold;
	}
	.modal-wrap{
		z-index: 100;
		position: fixed;
		top: 150px;
		width: 700px;
		padding: 20px 30px;
		background-color: white;
		border-radius: 15px;
		font-family: 'Open Sans', sans-serif;
	}

	.modal-header{
		display: flex;
		justify-content: space-between;
		padding: 0;
	}

	.modal-table{
		font-size: 1.2em;
		margin-top: 20px;
	}

	.modal-body{
		padding: 0;
		margin-top: 20px;
	}

	.modal-btn{
		padding: 8px 30px;
		margin-top: 15px;
	}

	i{
		cursor: pointer;
	}
	.right{
		text-align: left;
		padding-left: 20px;
	}

	.left{
		text-align: right;
		width: 200px;
	}
	tr{
		height: 40px;
		font-size: 1.1em;
	}
</style>
