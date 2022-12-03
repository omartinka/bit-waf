<template>
  <div class="endpoint">
    Endpoint: {{ path }} <br>
    Rules:
    <select class="select" v-model="new_rule">
      <option v-for="rule in ruletypes">{{rule}}</option>
    </select>
    <select class="select" v-model="direction">
      <option v-for="direction in ['in', 'out']">{{direction}}</option>
    </select>
    <button @click="add_rule()">Add</button>

    <div v-for="rule of rules">
      {{ rule.dir }}: {{ rule.type }}
      <button @click="remove(rule)">❌</button>
    </div>
    
  </div>
</template>

<script>
export default {
  name: "Endpoint",
  props: {
    path: ""
  },
  data() {
    return {
      direction: "",
      new_rule: "",
      rules: [],
      ruletypes: [
        'xss', 'sqli'
      ]
    }
  },
  methods: {
    add_rule() {
      if (this.new_rule == "" || this.direction == "") {
        return;
      }
      for (let rule of this.rules) {
        if (rule.type == this.new_rule && rule.dir == this.direction) {
          return;
        }
      }
      this.rules.push({
        type: this.new_rule,
        dir: this.direction
      });
    },
    get_config() {
      let obj = {
        "path": this.path,
        "rules": []
      }
      for (let x of this.rules) {
        obj['rules'].push(x)
      }
      return obj;
    },
    remove(rule) {
      this.rules = this.rules.filter(x => x != rule);
    }
  }
}
</script>

<style>
.endpoint {
  outline: 1px solid black;
  margin: 10px;
  padding: 5px;
}
.select {
  width: 100px;
}
</style>