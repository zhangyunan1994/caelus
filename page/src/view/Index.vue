<template>
  <div style="height: 100%;">
    <header>

    </header>
    <el-row :gutter="10">
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
  </div>
</template>

<script>
  import {
    getConnection,
    getDatabase,
    getTable,
    getColumn
  } from "@/api/"

  export default {
    name: 'Index',
    watch: {
      filterText(val) {
        this.$refs.tree2.filter(val);
      }
    },
    data() {
      return {
        tableHeight: 500,
        filterText: '',
        columns: [],
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
      loadNode1(node, resolve) {
        console.info(node)
        if (node.level === 0) {
          // 第一层 加载所有的连接
          getConnection().then(response => {
            let connections = Array.prototype.map.call(response.data, item => {
              return {"label": item['name'], "connection": item['id']}
            })
            return resolve(connections)
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
          console.info(response)
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
