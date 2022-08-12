def validate_size(drone_class, exception):
    """Check that the maximum number of drones doesn't exceed 10"""
    size = drone_class.objects.count()
    if size > 10:
        raise exception("The maximum allowable drone a fleet is 10")
