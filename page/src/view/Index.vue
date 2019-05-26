<template>
  <div style="height: 100%;">
    <header>
      <el-row>
        <el-col :span="4">
          &nbsp;
        </el-col>
        <el-col :span="16" align="center">
          <div class="searchInput">
            <el-input @change="search" placeholder="请输入内容" v-model="selected_column" class="searchClass">
              <div slot="prepend">
                <div class="centerClass">
                  <el-select v-model="selected_connection" placeholder="请选择" style="width: 120px">
                    <el-option :label="con.label" :value="con.connection" v-for="con in connections"></el-option>
                  </el-select>
                </div>
                <div class="centerClass">
                  <div class="line"></div>
                </div>
              </div>
              <el-button slot="append" icon="el-icon-search"></el-button>
            </el-input>
          </div>
        </el-col>
        <el-col :span="4">
          <el-button plain icon="el-icon-plus" @click="dialogFormVisible = true">Add Connection</el-button>
        </el-col>
      </el-row>
    </header>
    <el-row :gutter="10" class="aside">
      <el-col :span="4">
        <aside>
          <el-input
            placeholder="输入关键字进行过滤"
            v-model="filterText">
          </el-input>
          <div class="database-tree">
            <el-tree
              class="filter-tree"
              :props="defaultProps"
              :load="loadNode1"
              lazy
              :highlight-current="true"
              :filter-node-method="filterNode"
              @node-click="handleNodeClick"
              ref="tree2">
            </el-tree>
          </div>
        </aside>
      </el-col>
      <el-col :span="20">
        <section>
          <div v-show="false"></div>
          <div v-show="true">
            <el-table
              :data="columns"
              :height="tableHeight"
              border
              stripe
              style="width: 100%">
              <el-table-column
                prop="table"
                label="table"
                width="200" v-if="show_table">
              </el-table-column>
              <el-table-column
                prop="column"
                label="column"
                width="200">
              </el-table-column>
              <el-table-column
                prop="nullable"
                label="nullable"
                width="80">
              </el-table-column>
              <el-table-column
                prop="type"
                label="type"
                width="170">
              </el-table-column>
              <el-table-column
                prop="default"
                label="default"
                width="130">
              </el-table-column>
              <el-table-column
                prop="comment"
                label="comment">
              </el-table-column>
            </el-table>
          </div>
        </section>
      </el-col>
    </el-row>
    <el-dialog title="连接信息" :visible.sync="dialogFormVisible">
      <el-form :model="connection">
        <el-form-item label="连接名称" :label-width="formLabelWidth">
          <el-input v-model="connection.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="host" :label-width="formLabelWidth">
          <el-input v-model="connection.host"></el-input>
        </el-form-item>
        <el-form-item label="port" :label-width="formLabelWidth">
          <el-input v-model="connection.port"></el-input>
        </el-form-item>
        <el-form-item label="user" :label-width="formLabelWidth">
          <el-input v-model="connection.user"></el-input>
        </el-form-item>
        <el-form-item label="password" :label-width="formLabelWidth">
          <el-input v-model="connection.password"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false, connection = {}">取 消</el-button>
        <el-button type="primary" @click="addConnection">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import {
    getConnection,
    getDatabase,
    getTable,
    getColumn,
    getConnectionColumn,
    addConnection
  } from "@/api/"

  export default {
    name: 'Index',
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      },
      selected_column(val) {
        this.search();
      },
      selected_connection(val) {
        this.search();
      }
    },
    data() {
      return {
        dialogFormVisible: false,
        formLabelWidth: '120px',
        selected_connection: null,
        selected_column: null,
        show_table: false,
        tableHeight: 500,
        filterText: '',
        columns: [],
        connections: [],
        connection: {},
        defaultProps: {
          children: 'children',
          label: 'label',
          isLeaf: 'leaf'
        }
      };
    },
    mounted: function () {
      this.tableHeight = window.innerHeight - 100;
    },
    methods: {
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      addConnection() {
        addConnection(this.connection).then(response => {
          console.info(response)
          getConnection().then(response => {
            this.connections = Array.prototype.map.call(response.data, item => {
              return {"label": item['name'], "connection": item['id']}
            })
          })
        })
        this.dialogFormVisible = false
        this.connection = {}
      },
      search() {
        if (!this.selected_connection) return
        if (!this.selected_column) return
        getConnectionColumn(this.selected_connection, this.selected_column).then(response => {
          this.show_table = true
          this.columns = response.data
        })
      },

      loadNode1(node, resolve) {
        if (node.level === 0) {
          // 第一层 加载所有的连接
          getConnection().then(response => {
            this.connections = Array.prototype.map.call(response.data, item => {
              return {"label": item['name'], "connection": item['id']}
            })
            return resolve(this.connections)
          })
        } else if (node.level === 1) {
          getDatabase(node.data.connection).then(response => {
            let databases = Array.prototype.map.call(response.data, item => {
              return {"label": item, "database": item, "connection": node.data.connection}
            })
            return resolve(databases)
          })
        } else if (node.level === 2) {
          getTable(node.data.connection, node.data.database).then(response => {
            let tables = Array.prototype.map.call(response.data, item => {
              return {
                "leaf": true,
                "label": item['name'],
                "table": item['name'],
                "database": node.data.database,
                "connection": node.data.connection
              }
            })
            return resolve(tables)
          })
        } else {
          return resolve([])
        }
      },
      handleNodeClick(data, node, ori) {
        if (node.level !== 3) return
        getColumn(data.connection, data.database, data.table).then(response => {
          this.show_table = false
          this.columns = response.data
        })
      }
    }
  }
</script>

<style>
  header {
    height: 60px !important;
    background-color: #252e2f;
    line-height: 60px;
  }

  .aside {
    padding: 10px;
    margin: 0;
  }

  .el-tree--highlight-current .el-tree-node.is-current > .el-tree-node__content {
    background-color: #e4323278 !important;
  }

  .database-tree {
    padding-top: 5px;
    height: calc(100vh - 140px);
    overflow: auto;
  }

  .database-tree::-webkit-scrollbar {
    display: none;
  }

  .searchInput {
    min-width: 300px;
    max-width: 500px;
  }

  .searchClass {
    border: 1px solid #c5c5c5;
    border-radius: 20px;
    background: #f4f4f4;
  }

  .searchClass .el-input-group__prepend {
    border: none;
    background-color: transparent;
    padding: 0 10px 0 30px;
  }

  .searchClass .el-input-group__append {
    border: none;
    background-color: transparent;
  }

  .searchClass .el-input__inner {
    height: 36px;
    line-height: 36px;
    border: none;
    background-color: transparent;
  }

  .searchClass .el-icon-search {
    font-size: 16px;
  }

  .searchClass .centerClass {
    height: 100%;
    line-height: 100%;
    display: inline-block;
    vertical-align: middle;
    text-align: right;
  }

  .searchClass .line {
    width: 1px;
    height: 26px;
    background-color: #c5c5c5;
    margin-left: 14px;
  }

  .searchClass:hover {
    border: 1px solid #D5E3E8;
    background: #fff;
  }

  .searchClass:hover .line {
    background-color: #D5E3E8;
  }

  .searchClass:hover .el-icon-search {
    color: #409eff;
    font-size: 16px;
  }
</style>
