$.fn.Chart__TreeMap = async function(name) {
  const elm = $(this)[0];
  const chart = echarts.init(elm);
  const template_data = $(`#${name}`);
  const md = new markdownit()
  const tokens = md.parse(template_data[0].innerText)
  chart.setOption((option = {
    tooltip: {},
    series: [
      {
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        name: 'Tech Map',
        type: 'treemap',
        visibleMin: 300,
        tooltip: {
          formatter: function(event) {
            return event.data.name;
          }
        },
        upperLabel: {
          show: true,
          color: '#fff'
        },
        itemStyle: {
          borderColor: '#fff'
        },
        levels: [
          {
            itemStyle: {
              borderColor: '#777',
              borderWidth: 1,
              gapWidth: 1,
            },
            upperLabel: {
              show: false
            }
          },
          {
            itemStyle: {
              borderColor: '#555',
              textBorder: null,
              borderWidth: 5,
              gapWidth: 1
            },
            emphasis: {
              itemStyle: {
                borderColor: '#ddd'
              }
            }
          },
          {
            itemStyle: {
              borderColor: '#555',
              textBorder: null,
              borderWidth: 5,
              gapWidth: 1
            },
            emphasis: {
              itemStyle: {
                borderColor: '#ddd'
              }
            }
          },
        ],
        data: tokensToJson(tokens),
      }
    ]
  }));
};
function string_to_slug (str) {
  // https://gist.github.com/codeguy/6684588
  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();
  // remove accents, swap ñ for n, etc
  var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
  var to   = "aaaaeeeeiiiioooouuuunc------";
  for (var i=0, l=from.length ; i<l ; i++) {
    str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }
  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
    .replace(/\s+/g, '-') // collapse whitespace and replace by -
    .replace(/-+/g, '-'); // collapse dashes
  return str;
}
function tokensToJson(tokens) {
  var current = null;
  for(var idx = 0; idx < tokens.length; idx++) {
    const token = tokens[idx];
    switch (token.type) {
      // There should only be one list to handle
      case 'bullet_list_open':
      case 'bullet_list_close':
      case 'paragraph_open':
      case 'paragraph_close':
        continue
      case 'inline':
        current.name = token.content
        current.path.push(string_to_slug(token.content))
        continue
      case 'list_item_open':
        if (current === null) {
          current = {
            parent: null,
            path: [],
          }
        } else {
          current = {
            parent: current,
            path: current.path.slice(),
          }
        }
        current.value = 1;
        current.children = [];
        continue
      case 'list_item_close':
        if (current === null) {
          console.error("Shouldn't happen")
        } else {
          if (current.parent !== null) {
            current.parent.children.push(current)
            current.path = current.path.join('/')
            if (current.children.length == 0) {
              delete current.children;
            }
            current = current.parent
          }
          for(var pdx = 0; pdx < current.children.length; pdx++) {
            const child = current.children[pdx];
            if(child.parent) { delete child.parent; }
          }
        }
        continue
      default:
        console.error('Not Handled', token.type);
        continue;
    }
  }
  return current.children;
}