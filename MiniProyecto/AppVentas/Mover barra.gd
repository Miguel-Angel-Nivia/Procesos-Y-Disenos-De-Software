extends Control

var following = false
var dragging_start_position = Vector2()

func _process(_delta):
	if following:
		var window = get_window()
		var new_position = Vector2(get_window().position) + get_global_mouse_position() - dragging_start_position
		window.set_position(new_position)

func _on_gui_input(event):
	if event is InputEventMouseButton:
		if event.get_button_index() == 1 and event.pressed:
			following = true
			dragging_start_position = get_local_mouse_position()
		elif event.get_button_index() == 1 and !event.pressed:
			following = false

