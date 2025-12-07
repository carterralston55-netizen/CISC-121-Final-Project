import gradio as gr


def merge_sort(arr):
    if len(arr) > 1:
        left = arr[:len(arr)//2]
        right = arr[len(arr)//2:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    return arr


def merge_sort_capture(arr, steps):
    steps.append(arr.copy())  # record before merge

    if len(arr) > 1:
        mid = len(arr)//2
        left = arr[:mid]
        right = arr[mid:]

        merge_sort_capture(left, steps)
        merge_sort_capture(right, steps)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

        steps.append(arr.copy()) # record after merge

    return arr



def render_bars(step, steps):
    arr = steps[step]
    html = "<div style='display:flex; align-items:flex-end; height:200px;'>"

    for v in arr:
        html += (
            f"<div title='{v}' "
            f"style='width:25px; margin:3px; background:#4CAF50;"
            f"height:{v*10}px'></div>"
        )

    html += "</div>"
    return html


def run_merge(text):
    nums = [int(x) for x in text.split(",")]
    steps = []
    merge_sort_capture(nums.copy(), steps)
    return steps, gr.update(minimum=0, maximum=len(steps)-1, step=1, value=0)



with gr.Blocks() as demo:
    gr.Markdown("Merge Sort Visualizer (Bar Chart)")

    input_arr = gr.Textbox(label="Enter numbers separated by commas e.g. (1,2,3)")
    run_button = gr.Button("Run Merge Sort")

    slider = gr.Slider(0, 1, step=1, label="Step")
    output_html = gr.HTML()
    steps_state = gr.State()

    run_button.click(fn=run_merge,
                     inputs=input_arr,
                     outputs=[steps_state, slider])

    slider.change(fn=render_bars,
                  inputs=[slider, steps_state],
                  outputs=output_html)

demo.launch()