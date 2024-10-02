from app.Models.brand import Brand, db

class BrandRepository:
    # GET
    def get_all(self):
        query = Brand.query.order_by(Brand.name.asc())
        return query.all()

    # GET by ID
    def get_by_id(id):
        return Brand.query.get_or_404(id)

    # POST
    @staticmethod
    def add_new(brand):
        db.session.add(brand)
        db.session.commit()
        return brand

    # PUT / PATCH
    @staticmethod
    def update_brand(brand, data):
        brand.name = data['name']
        brand.image = data['image']
        db.session.commit()

    # DELETE
    @staticmethod
    def remove_brand(brand):
        db.session.delete(brand)
        db.session.commit()