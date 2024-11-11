async function sleep(timeout) {
    await new Promise((resolve)=>{
        setTimeout(resolve, timeout * 1000);
    }
    );
}
;async function processRows() {

    for (let i = 0; i <= 29; i++) {

        var orignialWindowOpen = window.open;
        window.open = async function() {
            var taskid = i + 1
            var newWindow = orignialWindowOpen.apply(this, arguments);
            await sleep(1);
            // var newWindow = window;  //调试用
            // console.log("newWindow ", newWindow);
            // 100s 强制关闭
            setTimeout(()=>{
                if (!newWindow.closed) {
                    newWindow.close();
                    console.log("Manipulating Row", taskid, "Window closed at 100s");
                }
            }
            , 100000);

            var alerted = false;
            newWindow.confirm = (m)=>console.log('confirm', taskid, m);
            newWindow.alert = (m)=>{
                console.log('alert', taskid, m);
                alerted = true;
            }

            var isElLoaded = async sl=>{
                await sleep(0.05);
                if (newWindow.closed) {
                    throw taskid + "newWindow.closed"
                }
                while (newWindow.document.querySelector(sl) === null) {
                    await new Promise((resolve)=>{
                        requestAnimationFrame(resolve)
                    }
                    );
                }
                ;return newWindow.document.querySelector(sl);
            }
            ;
            function rrrand(min, max) {
                return Math.floor(Math.random() * (max - min + 1)) + min
            }
            ;function setValue(el, min, max) {
                if (!el || !el.value) {
                    el.value = rrrand(min, max).toFixed(1);
                }
            }
            ;await sleep(0.5);

            taskid = (await isElLoaded("#Name")).value + ' ' + taskid;

            (await isElLoaded("#d1 > div.fieldset1 > fieldset > div > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset15 > fieldset > div > div > label:nth-child(1) > input")).checked = true;

            (await isElLoaded("#d1 > div.fieldset3 > fieldset > legend > span.title_icon.plus_icon")).click();
            await sleep(1);
            (await isElLoaded("#d1 > div.fieldset3 > fieldset > div:nth-child(2) > div:nth-child(2) > div > label:nth-child(4) > input[type=radio]")).click();
            await sleep(0.3);
            (await isElLoaded("#d1 > div.fieldset3 > fieldset > div:nth-child(3) > div > label:nth-child(1) > input[type=radio]")).click();
            await sleep(0.3);
            (await isElLoaded("#d1 > div.fieldset3 > fieldset > div:nth-child(4) > div:nth-child(2) > div > label:nth-child(1) > input[type=radio]")).click();
            await sleep(0.3);
            (await isElLoaded("#yjqk")).click();
            await sleep(0.3);

            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(2) > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(3) > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(4) > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(5) > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(6) > div > label:nth-child(1) > input")).checked = true;
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(7) > div > label:nth-child(1) > input")).checked = true;

            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(8) > div > label:nth-child(1) > input[type=radio]")).click();
            await sleep(0.3);
            (await isElLoaded("#d1 > div.fieldset4 > fieldset > div:nth-child(9) > div > label:nth-child(1) > input[type=radio]")).click();
            await sleep(0.3);

            var sg = await isElLoaded("#sg");
            var tz = await isElLoaded("#tz");
            var yw = await isElLoaded("#yw");
            var age = await isElLoaded("#Age");
            var gender = await isElLoaded("#Gender");
            var xy1 = await isElLoaded("#xy1");
            var xy2 = await isElLoaded("#xy2");
            var isHypertension = (await isElLoaded('#d1 > div.fieldset1 > fieldset > div > div > label:nth-child(2) > input[type=checkbox]')).checked
            console.log(taskid, 'isHypertension', isHypertension)

            setValue(xy1, 110, 130);
            setValue(xy2, 75, 85);

            if (gender.value == '男') {
                setValue(sg, 165, 180);
                setValue(tz, 60, 80);
            } else {
                setValue(sg, 150, 170);
                setValue(tz, 50, 70);
            }
            ;var sgv = parseFloat(sg.value);
            var tzv = parseFloat(tz.value);
            var bmi = tzv / (sgv * sgv / 10000);
            var bzyw = sgv * bmi / 50;
            setValue(yw, bzyw, bzyw);

            (await isElLoaded("#span_btn_save")).click();

            while (!(await isElLoaded("#jjkzdqt")).value) {
                await sleep(1);
            }
            console.log(taskid, (await isElLoaded("#jjkzdqt")).value);

            (await isElLoaded("#A6")).click();
            console.log(taskid, alerted);
            alerted = false;
            while (!alerted) {
                await sleep(1);
            }
            (await isElLoaded("#sp3")).click();
            await sleep(2);
            (await isElLoaded("#span_btn_Scheme > a")).click();
            while ((await isElLoaded("#YXFAMAIN")).children.length < 2) {
                await sleep(1);
            }
            (await isElLoaded("#div_spn > span.buttons.btn_save6 > a")).click();

            console.log(taskid, '已选方案数量：', (await isElLoaded("#SchemeList > div")).children.length)
            newWindow.close();
            console.log("Manipulating Row", taskid, "Window closed");
            return newWindow;
        }

        console.log("Manipulating Row", i + 1);
        var currentRow = document.querySelector(`#dgvResult_${i}`);
        currentRow.click();
        showForm('ibtnUserDefine', 1);
        await sleep(30);

        window.focus();
        window.open = orignialWindowOpen;
    }
    ;
}
;async function limour_main() {
    while (true) {
        await processRows();
        document.querySelector("#QueryButton1_LinkButton1").click();
        await sleep(35);
    }
}
;limour_main()
