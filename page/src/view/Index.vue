<template>
  <div style="height: 100%;">
    <header>
      这是一个头
    </header>
    <el-row :gutter="20">
      <el-col :span="4">
        <aside>
          <el-input
            placeholder="输入关键字进行过滤"
            v-model="filterText">
          </el-input>
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
        </aside>
      </el-col>
      <el-col :span="20">
        <section>
          <div v-show="false"></div>
          <div v-show="true">
            <el-table
              :data="columns"
              height="1000"
              border
              stripe
              style="width: 100%">
              <el-table-column
                prop="column"
                label="column"
                width="180">
              </el-table-column>
              <el-table-column
                prop="nullable"
                label="nullable"
                width="180">
              </el-table-column>
              <el-table-column
                prop="type"
                label="type"
                width="180">
              </el-table-column>
              <el-table-column
                prop="default"
                label="default"
                width="180">
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
    },
    data() {
      return {
        filterText: '',
        columns: [],
        defaultProps: {
          children: 'children',
          label: 'label',
          isLeaf: 'leaf'
        }
      };
    }
  }
</script>

<style>
  header {
    height: 80px !important;
  }

  aside {
    width: 200px;
    height: 500px;
    overflow:auto;
  }

  aside::-webkit-scrollbar {
        display: none;
    }

  .el-tree--highlight-current .el-tree-node.is-current>.el-tree-node__content {
    background-color: #e4323278 !important;
  }
</style>
