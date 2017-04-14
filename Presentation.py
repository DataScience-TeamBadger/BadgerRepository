from pptx import Presentation

#Badger Data Science Presentation Code
#Presentation Conducted -
#Data Science - Alan Jamieson - COSC 480, Spring 2017

prs = Presentation('')
title_slide_layout = prs.slide_layouts[0]
slide = prs. slides.add_slide(title_slide_layout)
title = slide.shapes.title
subtitle = slide.placeholders[1]

title.text = "Maximizing Spending on Urban Mass Transportation"
subtitle.text = "Badger Data Science"

prs.save('BadgerDataScience_Presentation_01.pptx')
