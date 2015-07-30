"""Helper functions for views.py."""

def cascade_visibility_down(element, visibility_mode):
    """Sets visibility for all descendents of an element. (cascades down)."""

    # Find all related objects, and set them all to the appropriate visibility mode.
    links = [rel.get_accessor_name() for rel in element._meta.get_all_related_objects()]
    for link in links:
        objects = getattr(element, link).all()
        for object in objects:
            try:
                print("Examining object:", object)
                if visibility_mode == 'private':
                    if object.public:
                        object.public = False
                        object.save()
                        print("-- Set element private: ", object)
                elif visibility_mode == 'public':
                    if not object.public:
                        object.public = True
                        object.save()
                        print("-- Set element public: ", object)
            except Exception as e:
                # Must not be a public/ private object
                print("Can't set object private:", object, e)
            # Check if this object has related objects, if so use recursion
            if object._meta.get_all_related_objects():
                cascade_visibility_down(object, visibility_mode)

