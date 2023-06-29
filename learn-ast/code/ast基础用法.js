/*    js转化ast  parser解析   js解析为ast
import { parse } from "@babel/parser";
import fs from "fs";

const code = fs.readFileSync("code/code1.js","utf-8");
let ast = parse(code);
console.log(ast)
*/

/*  ast转化为js  generator还原  ast还原为js
import { parse } from "@babel/parser";
import generate from "@babel/generator";
import fs from "fs";

const code = fs.readFileSync("code/code1.js","utf-8");
let ast = parse(code);

const{ code: output } = generate(ast);
console.log(output)
*/

/*
  // ast遍历及修改 traverse遍历节点
import { parse } from "@babel/parser";
import traverse from "@babel/traverse";
import generate from "@babel/generator";
import fs from "fs";
const code = fs.readFileSync("code/code1.js","utf-8");
let ast = parse(code);

traverse(ast,{
// enter方法是每个节点被遍历时都会调用的方法，path是节点的相关信息,path属于NodePath类型，有node,partent等属性，node属性就是当前节点，partent就是父节点
    enter(path){
        let node = path.node
        if (node.type === "NumericLiteral" && node.value === 3){
            node.value = 5;
        }
        if (node.type === "StringLiteral" && node.value === "hello"){
            node.value = "hi";
        }
    }
});
const{ code: output } = generate(ast);
console.log(output)
*/
/*
  // ast遍历及修改删除 traverse遍历节点
import { parse } from "@babel/parser";
import traverse from "@babel/traverse";
import generate from "@babel/generator";
import fs from "fs";
const code = fs.readFileSync("code/code1.js","utf-8");
let ast = parse(code);

traverse(ast,{
// NumericLiteral方法是每个数字字面量节点被遍历时都会调用的方法，StingLiteral就是字符串字面量
    NumericLiteral(path){
        let node = path.node
        if (node.value === 3){
            node.value = 5;
        }
    },
    StringLiteral(path){
        let node = path.node
        if (node.value === "hello") {
            node.value = "hi";
        }
    },
    //删除console.log
    ExpressionStatement(path) {
        // ?.是可选链操作符  使用.查找属性时，找不到会报错。  使用?.找不到会返回undefined
        if(path.node?.expression?.callee?.object?.name === "console"){
            path.remove()
        }
    },

});
const{ code: output } = generate(ast);
console.log(output)
*/
/*
//节点插入
import { parse } from "@babel/parser";
import traverse from "@babel/traverse";
import generate from "@babel/generator";
import * as types from "@babel/types";
import fs from "fs";
const code = fs.readFileSync("code/code1.js","utf-8");
let ast = parse(code);

traverse(ast,{
    VariableDeclaration(path){
        console.log(11111)
        //通过下列判断找到const a = 3所在的节点
        if(path.node?.kind === "const" && path.node?.declarations[0]?.id?.name === "a" && path.node?.declarations[0]?.init?.value === 3){
            let init = types.binaryExpression(
            "+",
            types.identifier("a"),
            types.numericLiteral(1)
            );
            let declarator = types.variableDeclarator(types.identifier("b"),init);
            let declaration = types.variableDeclaration("const",[declarator]);
            path.insertAfter(declaration);  //使用insertAfter插入节点
            path.stop()  //找到了就不再找了，类似于循环中的break
            // path.replaceWith(declaration)//替换为新的节点
            // path.remove() // 删除当前节点
            // let copyNode = types.cloneNode(path.node);//复制当前节点
            // traverse(copyNode, {
            //     enter(path){
            //         console.log(333333);
            //     }
            // }, {}, path);// 对子树进行遍历和替换，不影响当前的path

        };
    },

});
const{ code: output } = generate(ast);
console.log(output)
*/







