<template>
    <div>
      <canvas ref="barChart"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    props: {
      data: {
        type: Array,
        required: true
      }
    },
    data() {
      return {
        chart: null
      };
    },
    mounted() {
      this.renderChart();
    },
    watch: {
      data() {
        this.renderChart();
      }
    },
    methods: {
      renderChart() {
        const ctx = this.$refs.barChart.getContext('2d');
        if (this.chart) {
          this.chart.destroy();
        }
        this.chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.data.map(item => item.section_name),
            datasets: [{
              label: 'Number of Books',
              data: this.data.map(item => item.books_count),
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    },
    beforeDestroy() {
      if (this.chart) {
        this.chart.destroy();
      }
    }
  };
  </script>
  
  