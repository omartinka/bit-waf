<script>
import Container from '/src/components/Container.vue';

export default {
  name: "App",
  data() {
    return {
      new_host: "",
      host_ip: "",
      hosts: [],
      config: []
    };
  },
  components: { Container },
  methods: {
    async get_rules() {
      this.config = [];
      for(let app of this.hosts) {
        let obj = {
          "host": app.host,
          "ip": app.ip,
          "ruleset": this.$refs[app.host][0].get_config()
        }
        this.config.push(obj);
      }
      await fetch('http://api.fw-management.local:8080/load', {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(this.config)
      });
    },
    add_host() {
      if (this.hosts.includes(this.new_host)) {
        alert('Application already configured.');
        this.new_host = "";
        return;
      }

      if (this.new_host == "" || this.host_ip == "") {
        alert('Application name cannot be empty.');
        return;
      }

      this.hosts.push({
        "host": this.new_host,
        "ip": this.host_ip
      });
      this.new_host = "";
      this.host_ip = "";
    },
    async load_rules() {
      const res = await fetch('http://api.fw-management.local:8080/rules')
      const data = await res.json()
      console.log(data);
    }
  }
}
</script>

<template>
  <div class="app">
    <div class="header">
      FW - Management<br>

      Hostname:
      <input v-model="new_host" type="text"><br>
      Internal IP:
      <input v-model="host_ip" type="text"><br>

      <button @click="add_host()">Add App</button>
      <button @click="load_rules()">Load</button>
      <button @click="get_rules()">Apply</button>
    </div>
    <div v-for="app in hosts" >
      <Container :ref="app.host" :host="app.host"></Container>
    </div>
  </div>
</template>

<style>
.header {
  padding: 5px;
  margin: 10px;
}
button {
  cursor: pointer;
  border: none;
  height: 20px;
  outline: 1px solid black;
  background-color: white;
  margin: 5px;
}
button:hover {
  transition: 0.3s;
  color: white;
  background-color: black;
}
</style>