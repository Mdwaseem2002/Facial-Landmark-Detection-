<template>
  <div>
    <h2>{{ msg }}</h2>
    <h1><p style="color: greenyellow;">HelloWorld.</p></h1>

    <!-- Button to fetch data -->
    <button @click="fetchData">Fetch Data</button>

    <!-- Display data in a table -->
    <table v-if="data.length > 0">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Password</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in data" :key="index">
          <td>{{ item.name }}</td>
          <td>{{ item.email }}</td>
          <td>{{ item.password }}</td>
        </tr>
      </tbody>
    </table>

    <router-link to="/">Go back to Form</router-link>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: 'Display Data',
      data: [], // Array to store fetched data
    };
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/');
        if (response.ok) {
          const jsonData = await response.json();
          this.data = jsonData;
          console.log('Data fetched successfully:', this.data);
        } else {
          console.error('Failed to fetch data.');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
  mounted() {
    // Fetch data when the component is mounted
    this.fetchData();
  },
};
</script>

<style scoped>
/* Your component-specific styles */
</style>
