// static/src/js/cash_dashboard.js
odoo.define('custom_cash_management.dashboard', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    
    var CashDashboard = AbstractAction.extend({
        template: 'CashDashboardMain',
        
        init: function(parent, context) {
            this._super(parent, context);
            this.dashboardData = {};
        },
        
        willStart: function() {
            var self = this;
            return $.when(
                this._super.apply(this, arguments),
                this._fetchDashboardData()
            );
        },
        
        _fetchDashboardData: function() {
            var self = this;
            return rpc.query({
                route: '/cash_management/dashboard_data',
            }).then(function(result) {
                self.dashboardData = result;
            });
        },
        
        start: function() {
            var self = this;
            return this._super.apply(this, arguments).then(function() {
                self._renderDashboard();
            });
        },
        
        _renderDashboard: function() {
            var self = this;
            this.$('.o_cash_dashboard_content').html(QWeb.render('CashDashboardContent', {
                widget: self,
            }));
            this._renderCashFlowChart();
        },
        
        _renderCashFlowChart: function() {
            var self = this;
            var ctx = this.$('.cash_flow_chart');
            
            // Lấy dữ liệu thu chi theo tháng qua RPC
            rpc.query({
                model: 'cash.receipt',
                method: 'get_monthly_data',
                args: [],
            }).then(function(data) {
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: data.labels,
                        datasets: [
                            {
                                label: 'Thu',
                                data: data.receipts,
                                borderColor: '#28a745',
                                fill: false
                            },
                            {
                                label: 'Chi',
                                data: data.payments,
                                borderColor: '#dc3545',
                                fill: false
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        title: {
                            display: true,
                            text: 'Biểu đồ thu chi theo tháng'
                        }
                    }
                });
            });
        },
    });
    
    core.action_registry.add('cash_dashboard', CashDashboard);
    return CashDashboard;
    
    });