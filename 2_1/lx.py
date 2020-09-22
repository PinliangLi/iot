import gpio_class

def write(servo, pulse):
    gpio_class.write(servo, pulse)

write(1, 200)