function tea(){
    window.location.href = "http://www.coffeen.cn/coffee/tea_item/";
}

function coffee(){
    window.location.href = "http://www.coffeen.cn/coffee/coffee_item/";
}

function pacakge(){
    window.location.href = "http://www.coffeen.cn/coffee/package/";
}


function add_cart(drinking_id,drinking_name,drinking_price,drinking_is_saled,drinking_limit_count){
   var html = "";
   var html_info = "";
   var index = 1;
   //每次添加购物车时存储数据为session,返回时构建购物车页面html
   $.ajax({
        type:"POST",
        url:"/coffee/store_cart_data/",
        dataType:'json',
        data: {'index':index,'drinking_price':drinking_price,'drinking_name':drinking_name,'drinking_id':drinking_id ,'drinking_is_saled':drinking_is_saled,'drinking_limit_count':drinking_limit_count},
        success:function(res){
            if(res.status == "ok"){
                $("#cart").empty();
                $("#cart_info").hide();
                html += '<div style="display: block;" id="first_level_cart"><div class="container"><div style="margin: 10px;">'
                    + '<div style="display:inline-block;float: left;" id="total_count">'
                    + '<img src="/static/image/cart.png" style="width: 40px;">'+res.first_level_cart_info.count+''
                    + '</div><div style="display:inline-block;margin-left: 50px;margin-top: 13px;">'
                    + '<p id="total_price">共 ￥'+res.first_level_cart_info.price+'</p>'
                    + '</div><div style="display:inline-block;float: right;"><input type="button" class="btn btn-warning" style="margin-top: 8px;" value="结算" onclick="href_to_balance_cart()">'
                    + '</div></div></div></div>';
                //res.first_level_cart_info
                $("#cart").append(html);
                $("#cart").show();
                //购买详细信息
                $("#first_level_cart").click(function(){
                    get_cart_session();
                });
            }
            else{
            }
        },
        error:function(result){
            alert("请求出错")
        }
    });
}

//获取购物车信息
function get_cart_session(){
    var plus = "plus";
    var minus = "minus";
    $.ajax({
         type:"GET",
         url:"/coffee/get_cart_session/",
         dataType:'json',
         success:function(res2){
             $("#cart_info").empty();
             second_level_cart_info = res2.second_level_cart_info;
             html_info = '<div class="container" style="margin-top: 10px;margin-bottom: 10px"><div style="padding:5px"><div><div style="display:inline-block;font-weight: bold;">已选饮品</div><div style="display:inline-block;float: right;margin-right: 10px;" onclick="delete_all_cart_session()"><span class="icon-trash"></span><span style="margin-left: 10px;font-weight: bold;">清空</span></div></div>';
             for(var cart_info in second_level_cart_info){
                 html_info += '<div class="row second_cart_info" id='+second_level_cart_info[cart_info].drinking_id+' style="margin-top:15px;"><div class="col-xs-6">'+second_level_cart_info[cart_info].drinking_name+'</div><div class="col-xs-2">￥'+second_level_cart_info[cart_info].drinking_price+'</div><div class="col-xs-4"><span><img src="/static/image/minus.png" style="width: 15px;margin-bottom: 4px;margin-right: 15px;" onclick=modify_drinking_count('+second_level_cart_info[cart_info].drinking_id+','+second_level_cart_info[cart_info].drinking_price+',1,"l_1","",1)></span><span class='+second_level_cart_info[cart_info].drinking_id+'>'+second_level_cart_info[cart_info].drinking_count+'</span><span><img src="/static/image/add.png" style="width: 15px;margin-bottom: 4px;margin-left: 15px;" onclick=modify_drinking_count('+second_level_cart_info[cart_info].drinking_id+','+second_level_cart_info[cart_info].drinking_price+',2,"l_1","",1)></span></div></div>';
             }
             html_info += '</div></div>';
             $("#cart_info").append(html_info);
             $("#cart_info").toggle(1);
             $("#cart_info").show();

         },
         error:function(res){
         
         }
    });
}


//清空购物车
function delete_all_cart_session(){
    $.ajax({
         type:"GET",
         url:"/coffee/delete_cart_session/",
         //dataType:'json',
         success:function(res){
               if(res == 'ok'){
                    //清空购物车
                    $("#cart_info").empty();
                    $("#cart").empty();
                    //隐藏购物车
                    $("#cart_info").hide();
                    $("#cart").hide();
               }
         }
    });
}

//减去饮品数量
function modify_drinking_count(drinking_id,drinking_price,type,level,max_coupon,modify_type){
    //查看饮品数量
    drinking_count = view_dringking_count(drinking_id);
    //如果更改的为结算页面的饮品数量则必须满足最少为1杯，所以判断此处为1杯时不调用后台方法，满足条件为：减法操作+当前仅有1杯+更改类型为结算时更改饮品类型
    if(modify_type == 2 && drinking_count == 1 && type == 1){
            console.log("no excuate");
    }
    else{
        //更改饮品数量
        $.ajax({
            type:"POST",
            url:"/coffee/modify_cart_data/",
            dataType:'json',
            data: {'drinking_id':drinking_id,'drinking_count':drinking_count,'type':type,'level':level},
            success:function(result){
                //改变界面中饮品数额和价格
                if(result.status == "ok"){
                   if(level == "l_1"){
                        //second_cart_info中数据更改
                        if(type == 1){ 
                             //判断如果仅有一行数据并且饮品数量仅为1个，则删除菜单选项，清session
                             var remain_line = $("div.row.second_cart_info").length;
                             count = $("span."+drinking_id+"").text();
                             if(remain_line == 1){
                                  if(count == 1){     
                                      delete_all_cart_session();
                                      return;
                                  }
                             }
                             //如果某行数据饮品数量为1个，则删除本行数据，否则本行饮品数量减1
                             if(count == 1){
                                  $("div#"+drinking_id+"").remove();
                             }
                             else{
                                  second_level_cart_info = result.second_level_cart_info;
                                  for(var res in second_level_cart_info){
                                      if(second_level_cart_info[res].drinking_id == drinking_id){
                                          $("span."+drinking_id+"").text(second_level_cart_info[res].drinking_count);
                                      }
                                  }
                             }
                         } 
                         else{
                             second_level_cart_info = result.second_level_cart_info;
                             for(var res in second_level_cart_info){
                                 if(second_level_cart_info[res].drinking_id == drinking_id){
                                     $("span."+drinking_id+"").text(second_level_cart_info[res].drinking_count);
                                 }
                             }
                         }
                        
                         //first_level_cart_info中数据更改
                         var html_count = '<img src="/static/image/cart.png" style="width: 40px;">'+result.first_level_cart_info.count+'';
                         var html_price = '共 '+result.first_level_cart_info.price+'';
                         $("#total_count").html(html_count);
                         $("#total_price").html(html_price)
                    }
                   
                   else{
                       //减法操作
                       if(type == 1){
                            count = $("span."+drinking_id+"").text();
                            //如果某行数据饮品数量为1个，则删除本行数据，否则本行饮品数量减1
                            if(count != 1){
                                 //$("div#"+drinking_id+"").remove();
                                 second_level_cart_info = result.second_level_cart_info;
                                 for(var res in second_level_cart_info){
                                     if(second_level_cart_info[res].drinking_id == drinking_id){
                                         $("span."+drinking_id+"").text(second_level_cart_info[res].drinking_count);
                                     }
                                 }
                            }
                       }
                       //加法操作
                       else{
                             second_level_cart_info = result.second_level_cart_info;
                             for(var res in second_level_cart_info){
                                 if(second_level_cart_info[res].drinking_id == drinking_id){
                                     $("span."+drinking_id+"").text(second_level_cart_info[res].drinking_count);
                                 }
                             }
                       }
                        var html_price = '￥ '+result.first_level_cart_info.price+'';
                        $("#total_price").html(html_price)
                        //无代金券使用
                        if(max_coupon == "no_coupon"){
                            $("#settlement_price").text(html_price)
                            $("#last_price").text("结算金额："+ html_price);
                            $("#total").val(result.first_level_cart_info.price);
                        }
                        //有代金卷使用
                        else{
                            var actual_price = (parseFloat(''+result.first_level_cart_info.price+'') - parseFloat(max_coupon)).toFixed(2);
                            $("#settlement_price").text('￥' + actual_price + '')
                            $("#last_price").text("结算金额：￥ "+ actual_price + '');
                            $("#total").val(actual_price);
                        }
                        //var actual_price = '+result.first_level_cart_info.price+' - coupon
                    
                    }
                }
                
            },
            error:function(res){
                console.log(res);
            }
        });
    }
}

//查看饮品目前数量
function view_dringking_count(drinking_id){
     var drinking_count = 0;
     $.ajax({
         type:"GET",
         url:"/coffee/get_cart_session/",
         dataType:'json',
         async:false,
         success:function(res){
           second_level_cart_info = res.second_level_cart_info
           for(var result in second_level_cart_info){
                if(second_level_cart_info[result].drinking_id == drinking_id){
                    drinking_count = second_level_cart_info[result].drinking_count
                }
           }
         },
         error:function(res){
         
         }
    });
    return drinking_count;
}


function generate_extraction_code(coffee_id,coffee_count,type){
     //根据是否提取过验证码跳转不同页面
     var btn_value = $("#"+coffee_id+"").val();
     if(btn_value == "查看提货码"){
        url = "http://www.coffeen.cn/coffee/get_code/"+coffee_id+"/"+coffee_count+"/"+type+"";
        window.location.href = url;
     }
     else{
        url = "http://www.coffeen.cn/coffee/generate_extraction_code/"+coffee_id+"/"+coffee_count+"/"+type+"";
        window.location.href = url;
     }

}

function href_to_coffee_item(){
    url = "http://www.coffeen.cn/coffee/coffee_item/";
    window.location.href = url;
}


function href_to_balance_cart(){
    url = "http://www.coffeen.cn/coffee/balance_cart_stuff";
    window.location.href = url;
}
